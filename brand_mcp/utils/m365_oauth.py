"""Microsoft 365 / Graph OAuth helpers.

Supports two flows:

1. **Client credentials** (application permissions) — simplest for internal-only
   servers where the SharePoint library is accessible to the app itself. Used
   by default when no per-user token is present.

2. **Authorization Code + PKCE** (delegated permissions) — for per-user
   scoped access. Tokens are kept in an in-process store keyed by ``user_id``.

For the Solidigm brand library (read-only shared content) client credentials
is sufficient. The delegated flow is wired up but optional.
"""
from __future__ import annotations

import asyncio
import base64
import hashlib
import logging
import secrets
import time
import urllib.parse
from typing import Any, Dict, Optional

import httpx

from ..config import config

log = logging.getLogger(__name__)

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
TOKEN_URL = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
AUTHORIZE_URL = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize"

# ---------------------------------------------------------------------------
# In-memory stores (swap for Redis / similar in production)
# ---------------------------------------------------------------------------
_user_tokens: Dict[str, Dict[str, Any]] = {}
_app_token: Dict[str, Any] = {}
_pending_auth: Dict[str, Dict[str, Any]] = {}


def init_store(_external_store: Optional[Any] = None) -> None:
    """Initialize the token store. Hook point for Redis-backed storage."""
    # Currently in-memory only; external backends can replace the module-level
    # dicts above or be wired in here.
    log.info("m365_oauth: in-memory token store initialized")


# ---------------------------------------------------------------------------
# Client-credentials flow (application-level access)
# ---------------------------------------------------------------------------
async def _fetch_app_token() -> str:
    """Fetch an app-level access token via client-credentials grant."""
    if not config.is_m365_configured:
        raise RuntimeError("M365 credentials not configured (see .env)")

    now = time.time()
    cached = _app_token.get("access_token")
    if cached and _app_token.get("expires_at", 0) > now + 60:
        return cached  # type: ignore[return-value]

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            TOKEN_URL.format(tenant=config.M365_TENANT_ID),
            data={
                "client_id": config.M365_CLIENT_ID,
                "client_secret": config.M365_CLIENT_SECRET,
                "scope": "https://graph.microsoft.com/.default",
                "grant_type": "client_credentials",
            },
        )
    resp.raise_for_status()
    data = resp.json()
    _app_token["access_token"] = data["access_token"]
    _app_token["expires_at"] = now + int(data.get("expires_in", 3300))
    return data["access_token"]


# ---------------------------------------------------------------------------
# Delegated flow (Authorization Code + PKCE)
# ---------------------------------------------------------------------------
def _pkce_pair() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(64)
    challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest())
        .rstrip(b"=")
        .decode()
    )
    return verifier, challenge


def build_authorize_url(user_id: str) -> str:
    """Return a URL users visit to start the delegated OAuth flow."""
    verifier, challenge = _pkce_pair()
    state = secrets.token_urlsafe(24)
    _pending_auth[state] = {"user_id": user_id, "verifier": verifier, "ts": time.time()}

    params = {
        "client_id": config.M365_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": f"{config.SERVER_BASE_URL}/microsoft/callback",
        "response_mode": "query",
        "scope": "offline_access User.Read Sites.Read.All",
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    return f"{AUTHORIZE_URL.format(tenant=config.M365_TENANT_ID)}?{urllib.parse.urlencode(params)}"


async def exchange_code(code: str, state: str) -> Dict[str, Any]:
    """Exchange an authorization code for tokens and store them keyed by user_id."""
    pending = _pending_auth.pop(state, None)
    if not pending:
        raise RuntimeError("Unknown or expired OAuth state")

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            TOKEN_URL.format(tenant=config.M365_TENANT_ID),
            data={
                "client_id": config.M365_CLIENT_ID,
                "client_secret": config.M365_CLIENT_SECRET,
                "code": code,
                "redirect_uri": f"{config.SERVER_BASE_URL}/microsoft/callback",
                "grant_type": "authorization_code",
                "code_verifier": pending["verifier"],
            },
        )
    resp.raise_for_status()
    data = resp.json()
    user_id = pending["user_id"]
    _user_tokens[user_id] = {
        "access_token": data["access_token"],
        "refresh_token": data.get("refresh_token", ""),
        "expires_at": time.time() + int(data.get("expires_in", 3300)),
    }
    return {"user_id": user_id}


async def _refresh_user_token(user_id: str) -> Optional[str]:
    tok = _user_tokens.get(user_id)
    if not tok or not tok.get("refresh_token"):
        return None

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            TOKEN_URL.format(tenant=config.M365_TENANT_ID),
            data={
                "client_id": config.M365_CLIENT_ID,
                "client_secret": config.M365_CLIENT_SECRET,
                "refresh_token": tok["refresh_token"],
                "grant_type": "refresh_token",
                "scope": "offline_access User.Read Sites.Read.All",
            },
        )
    if resp.status_code != 200:
        return None
    data = resp.json()
    _user_tokens[user_id] = {
        "access_token": data["access_token"],
        "refresh_token": data.get("refresh_token", tok["refresh_token"]),
        "expires_at": time.time() + int(data.get("expires_in", 3300)),
    }
    return data["access_token"]


async def _get_user_token(user_id: str) -> Optional[str]:
    tok = _user_tokens.get(user_id)
    if not tok:
        return None
    if tok["expires_at"] < time.time() + 60:
        return await _refresh_user_token(user_id)
    return tok["access_token"]


# ---------------------------------------------------------------------------
# Graph request with rate-limit handling
# ---------------------------------------------------------------------------
async def graph_request(
    path: str,
    *,
    user_id: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None,
    method: str = "GET",
) -> Dict[str, Any]:
    """Make an authenticated Graph API request.

    Prefers a per-user token when ``user_id`` is provided and one is cached;
    falls back to the client-credentials app token.
    """
    token: Optional[str] = None
    if user_id:
        token = await _get_user_token(user_id)
    if not token:
        token = await _fetch_app_token()

    url = f"{GRAPH_BASE}{path}" if path.startswith("/") else f"{GRAPH_BASE}/{path}"

    attempt = 0
    while True:
        attempt += 1
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.request(
                method,
                url,
                headers={"Authorization": f"Bearer {token}"},
                params=params,
            )

        if resp.status_code == 429 and attempt <= 3:
            retry_after = int(resp.headers.get("Retry-After", 2 ** attempt))
            log.warning("Graph 429, retrying in %ss (attempt %d)", retry_after, attempt)
            await asyncio.sleep(retry_after)
            continue

        if resp.status_code == 401 and user_id and attempt == 1:
            # User token may have expired — force refresh and retry once.
            new_token = await _refresh_user_token(user_id)
            if new_token:
                token = new_token
                continue

        resp.raise_for_status()
        if resp.headers.get("content-type", "").startswith("application/json"):
            return resp.json()
        return {"content": resp.content, "headers": dict(resp.headers)}


def is_user_authenticated(user_id: str) -> bool:
    return user_id in _user_tokens
