"""Solidigm Brand MCP server.

Exposes design tokens, brand guidelines, UI toolkit classes, local brand
assets, and SharePoint-hosted brand assets as MCP tools and resources.

Run locally::

    python -m brand_mcp.server

The server binds to ``MCP_HOST:MCP_PORT`` (defaults ``0.0.0.0:8080``) and
exposes:

- MCP tools: see ``mcp/tools/brand.py``
- MCP resources: ``brand://tokens/{colors,typography}``,
  ``brand://guidelines/main``, ``brand://assets/manifest``,
  ``brand://toolkit/css``
- HTTP routes for delegated OAuth: ``/microsoft/authorize``,
  ``/microsoft/callback``
- HTTP routes for the Astro site: ``/api/assets``
- HTTP route for the brand-compliance Skill: ``/api/validate`` (POST)
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict

from fastmcp import FastMCP

from .composer import assets as assets_mod
from .config import config
from .tools import brand as brand_tools
from .utils import m365_oauth

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s :: %(message)s",
)
log = logging.getLogger("solidigm.brand.mcp")

mcp = FastMCP(
    name="solidigm-brand",
    instructions=(
        "Canonical Solidigm brand system. Use these tools whenever a task "
        "involves Solidigm colors, typography, logos, illustrations, the UI "
        "toolkit, brand guidelines, or official brand SharePoint documents. "
        "Prefer structured resources (brand://...) for bulk reads; use tools "
        "for lookups, filters, or authenticated SharePoint queries."
    ),
)


# ---------------------------------------------------------------------------
# Tool registrations
# ---------------------------------------------------------------------------
@mcp.tool()
def get_design_tokens(category: str | None = None) -> Dict[str, Any]:
    """Return Solidigm design tokens. ``category`` ∈ {colors, typography} or omit for all."""
    return brand_tools.get_design_tokens(category)


@mcp.tool()
def get_color(name: str) -> Dict[str, Any]:
    """Look up a Solidigm brand color by name (e.g. 'Solidigm Purple', 'Electric Teal')."""
    return brand_tools.get_color(name)


@mcp.tool()
def get_brand_guidelines(topic: str | None = None) -> Dict[str, Any]:
    """Return Solidigm brand guidelines. Pass a ``topic`` to extract a specific section."""
    return brand_tools.get_brand_guidelines(topic)


@mcp.tool()
def get_ui_toolkit_class(name: str) -> Dict[str, Any]:
    """Return the CSS rules for a Solidigm UI toolkit class (e.g. 'tk-btn--primary')."""
    return brand_tools.get_ui_toolkit_class(name)


@mcp.tool()
async def list_assets(
    category: str | None = None,
    include_sharepoint: bool = True,
) -> Dict[str, Any]:
    """List brand assets. Optional ``category`` ∈ {logo, illustration, icon, image, template, product-render, doc}."""
    return await brand_tools.list_assets(category, include_sharepoint)


@mcp.tool()
async def get_asset(
    name: str | None = None,
    path: str | None = None,
    category: str | None = None,
) -> Dict[str, Any]:
    """Retrieve a single brand asset by name or exact path.

    Use ``name`` for a substring match (e.g. 'purple ppt icons', 'product render P5336').
    Use ``path`` for the exact ``rel_path`` returned by ``list_assets``.
    Optionally narrow with ``category`` ∈ {logo, illustration, icon, image, template, product-render, doc}.
    Returns ``download_url`` (SharePoint, ~1 hr) or ``url`` (local public path).
    """
    return await brand_tools.get_asset(name, path, category)


@mcp.tool()
def get_logo(
    variant: str = "standard",
    color: str = "purple",
    resolution: str | None = None,
    fmt: str = "png",
) -> Dict[str, Any]:
    """Resolve a specific Solidigm logo file.

    variant ∈ {s-mark, standard, stacked, wordmark}, color ∈ {black, purple, blue, white},
    resolution e.g. '1920x1080' (omit for svg/eps), fmt ∈ {png, svg, eps}.
    """
    return brand_tools.get_logo(variant, color, resolution, fmt)


@mcp.tool()
def get_brand_context(
    platform: str | None = None,
    task: str | None = None,
) -> Dict[str, Any]:
    """Return curated Solidigm brand guidelines scoped to a platform and task.

    platform ∈ {marketing, web-nextjs, web-react}, task ∈ {ui, copy, design, review, chart}.
    Omit both for full brand context.
    """
    return brand_tools.get_brand_context(platform, task)


@mcp.tool()
def validate_brand_output(
    content: str,
    platform: str | None = None,
) -> Dict[str, Any]:
    """Validate AI-generated content against Solidigm brand quality gates.

    Returns pass/fail with specific errors and warnings.
    """
    return brand_tools.validate_brand_output(content, platform)


@mcp.tool()
def get_brand_system_prompt(
    platform: str | None = None,
    include_design_rules: bool = True,
) -> Dict[str, Any]:
    """Return a pre-built Solidigm brand-aware LLM system prompt.

    Inject into system messages to ensure brand-compliant AI output.
    """
    return brand_tools.get_brand_system_prompt(platform, include_design_rules)


# Only register the SharePoint tool when the server is configured for it
if config.is_brand_sharepoint_configured:
    @mcp.tool()
    async def search_brand_source_documents(
        folder: str = "",
        name_filter: str = "",
    ) -> Dict[str, Any]:
        """Search the official Solidigm brand SharePoint library.

        Returns per-file ``web_url`` and a temporary ``download_url``.
        """
        return await brand_tools.search_brand_source_documents(folder, name_filter)


# ---------------------------------------------------------------------------
# MCP resources — canonical reads exposed as brand://...
# ---------------------------------------------------------------------------
@mcp.resource("brand://tokens/colors")
def _resource_colors() -> str:
    return json.dumps(brand_tools.get_design_tokens("colors")["tokens"], indent=2)


@mcp.resource("brand://tokens/typography")
def _resource_typography() -> str:
    return json.dumps(brand_tools.get_design_tokens("typography")["tokens"], indent=2)


@mcp.resource("brand://guidelines/main")
def _resource_guidelines() -> str:
    result = brand_tools.get_brand_guidelines()
    return result.get("content", "")


@mcp.resource("brand://toolkit/css")
def _resource_toolkit() -> str:
    path = os.path.join(config.docs_dir, "ui-toolkit.min.css")
    if not os.path.isfile(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


@mcp.resource("brand://assets/manifest")
def _resource_manifest() -> str:
    return json.dumps(assets_mod.list_local_assets(), indent=2)


# ---------------------------------------------------------------------------
# HTTP routes — OAuth callbacks + Astro site API
# ---------------------------------------------------------------------------
@mcp.custom_route("/microsoft/authorize", methods=["GET"])
async def microsoft_authorize(request):  # type: ignore[no-untyped-def]
    from starlette.responses import RedirectResponse
    user_id = request.query_params.get("user_id", "anonymous")
    return RedirectResponse(m365_oauth.build_authorize_url(user_id))


@mcp.custom_route("/microsoft/callback", methods=["GET"])
async def microsoft_callback(request):  # type: ignore[no-untyped-def]
    from starlette.responses import HTMLResponse
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    if not code or not state:
        return HTMLResponse("Missing code or state", status_code=400)
    try:
        await m365_oauth.exchange_code(code, state)
    except Exception as exc:  # noqa: BLE001
        return HTMLResponse(f"Auth failed: {exc}", status_code=400)
    return HTMLResponse(
        "<h2>Signed in</h2><p>You can close this tab.</p>"
        "<script>setTimeout(() => window.close(), 1200);</script>"
    )


@mcp.custom_route("/api/assets", methods=["GET"])
async def api_assets(request):  # type: ignore[no-untyped-def]
    """HTTP endpoint consumed by the Astro /assets page."""
    from starlette.responses import JSONResponse

    category = request.query_params.get("category")
    include_sp = request.query_params.get("sharepoint", "true").lower() != "false"
    result = await brand_tools.list_assets(category=category, include_sharepoint=include_sp)
    response = JSONResponse(result)
    # Allow the Astro site on any origin to read this (internal VPN-only deployment).
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Cache-Control"] = "public, max-age=300"
    return response


@mcp.custom_route("/api/health", methods=["GET"])
async def api_health(_request):  # type: ignore[no-untyped-def]
    from starlette.responses import JSONResponse
    return JSONResponse(
        {
            "status": "ok",
            "m365_configured": config.is_m365_configured,
            "sharepoint_configured": config.is_brand_sharepoint_configured,
        }
    )


@mcp.custom_route("/api/thumb", methods=["GET"])
async def api_thumb(request):  # type: ignore[no-untyped-def]
    """Proxy a SharePoint pre-signed image URL to avoid browser CORS restrictions.

    Usage: GET /api/thumb?url=<encoded-sharepoint-download-url>
    """
    import urllib.parse
    from starlette.responses import Response

    raw = request.query_params.get("url", "")
    if not raw:
        return Response("missing url", status_code=400)

    # Safety: only proxy *.sharepoint.com URLs
    parsed = urllib.parse.urlparse(raw)
    if not parsed.hostname or not parsed.hostname.endswith(".sharepoint.com"):
        return Response("forbidden", status_code=403)

    try:
        import httpx  # type: ignore[import]
        async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
            resp = await client.get(raw)
            content_type = resp.headers.get("content-type", "image/jpeg")
            return Response(
                content=resp.content,
                media_type=content_type,
                headers={"Access-Control-Allow-Origin": "*", "Cache-Control": "public, max-age=3600"},
            )
    except Exception as exc:  # noqa: BLE001
        log.warning("thumb proxy failed: %s", exc)
        return Response("proxy error", status_code=502)


@mcp.custom_route("/api/validate", methods=["POST", "OPTIONS"])
async def api_validate(request):  # type: ignore[no-untyped-def]
    """HTTP endpoint consumed by the brand-compliance Skill audit script.

    POST body: { "content": "<string>", "platform": "<optional>" }
    """
    from starlette.responses import JSONResponse, Response

    if request.method == "OPTIONS":
        return Response(
            status_code=204,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "content-type",
            },
        )

    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"status": "error", "message": "invalid JSON body"}, status_code=400)

    content = body.get("content")
    if not isinstance(content, str) or not content:
        return JSONResponse(
            {"status": "error", "message": "missing or empty 'content' field"},
            status_code=400,
        )
    platform = body.get("platform")

    result = brand_tools.validate_brand_output(content, platform)
    response = JSONResponse(result)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
async def _prewarm_cache() -> None:
    """Populate the SharePoint asset cache so the first user request is fast."""
    try:
        log.info("Pre-warming SharePoint asset cache…")
        await assets_mod.list_sharepoint_assets()
        log.info("SharePoint asset cache warm.")
    except Exception as exc:  # noqa: BLE001
        log.warning("Cache pre-warm failed (will retry on first request): %s", exc)


def main() -> None:
    import asyncio
    import threading

    m365_oauth.init_store()
    log.info(
        "Starting Solidigm Brand MCP on %s:%d (sharepoint=%s)",
        config.MCP_HOST,
        config.MCP_PORT,
        config.is_brand_sharepoint_configured,
    )

    # Kick off cache pre-warm in a background thread so it doesn't block startup.
    if config.is_brand_sharepoint_configured:
        def _run_prewarm() -> None:
            asyncio.run(_prewarm_cache())
        threading.Thread(target=_run_prewarm, daemon=True, name="cache-prewarm").start()

    mcp.run(transport="http", host=config.MCP_HOST, port=config.MCP_PORT)


if __name__ == "__main__":
    main()
