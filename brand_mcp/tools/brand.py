"""Brand MCP tool registrations.

These wrap the lower-level ``composer`` + token-reading helpers and present
them as MCP tools callable by AI agents (Claude, Cursor, VS Code Copilot, …).
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, List, Optional

from ..composer import assets as assets_mod
from ..composer import colors as colors_mod
from ..composer import context as context_mod
from ..composer import prompts as prompts_mod
from ..composer import validation as validation_mod
from ..config import config
from ..utils import m365_oauth

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Token helpers — read directly from the repo
# ---------------------------------------------------------------------------
def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


_TOKEN_CATEGORIES = (
    "colors", "typography", "space", "breakpoints", "radius",
    "shape", "motion", "elevation", "semantic", "icons", "voice",
)


def get_design_tokens(category: Optional[str] = None) -> Dict[str, Any]:
    """Return Solidigm design tokens.

    Parameters
    ----------
    category : str, optional
        One of: ``colors``, ``typography``, ``space``, ``breakpoints``,
        ``radius``, ``shape``, ``motion``, ``elevation``, ``semantic``,
        ``icons``. Omit for all non-index token files.
    """
    tokens_dir = config.tokens_dir
    if category:
        name = category.lower()
        path = os.path.join(tokens_dir, f"{name}.json")
        if not os.path.isfile(path):
            return {
                "status": "error",
                "error": f"Unknown token category: {category}",
                "valid_categories": list(_TOKEN_CATEGORIES),
            }
        return {"status": "ok", "category": name, "tokens": _read_json(path)}

    all_tokens: Dict[str, Any] = {}
    for cat in _TOKEN_CATEGORIES:
        p = os.path.join(tokens_dir, f"{cat}.json")
        if os.path.isfile(p):
            all_tokens[cat] = _read_json(p)
    return {"status": "ok", "tokens": all_tokens}


# ---------------------------------------------------------------------------
# Convenience / primitive token look-up tools
# ---------------------------------------------------------------------------

def get_spacing(step: Optional[str] = None) -> Dict[str, Any]:
    """Return Solidigm spacing tokens.

    Parameters
    ----------
    step : str, optional
        A specific step key (``"4"``, ``"8"``, ``"16"``, etc.).  Omit for
        the full scale.
    """
    data = _read_json(os.path.join(config.tokens_dir, "space.json"))
    scale = data.get("space", {})
    if step is not None:
        token = scale.get(str(step))
        if token is None:
            return {
                "status": "not_found",
                "step": step,
                "available": list(scale.keys()),
            }
        return {"status": "ok", "step": step, **token}
    return {
        "status": "ok",
        "scale": {k: v.get("$value") for k, v in scale.items() if isinstance(v, dict)},
        "base_unit": data.get("$extensions", {}).get("com.solidigm.brand", {}).get("baseUnit", "4px"),
        "tokens": scale,
    }


def get_breakpoints() -> Dict[str, Any]:
    """Return the canonical Solidigm breakpoint + container-width tokens."""
    data = _read_json(os.path.join(config.tokens_dir, "breakpoints.json"))
    return {
        "status": "ok",
        "breakpoints": {k: v.get("$value") for k, v in data.get("breakpoint", {}).items() if isinstance(v, dict)},
        "containers": {k: v.get("$value") for k, v in data.get("container", {}).items() if isinstance(v, dict)},
        "tokens": data,
    }


def get_motion() -> Dict[str, Any]:
    """Return the Solidigm motion tokens (durations, easings, transforms)."""
    data = _read_json(os.path.join(config.tokens_dir, "motion.json"))
    durations = {k: v.get("$value") for k, v in data.get("duration", {}).items() if isinstance(v, dict)}
    easings = {k: v.get("$value") for k, v in data.get("easing", {}).items() if isinstance(v, dict)}
    transforms = {k: v.get("$value") for k, v in data.get("transform", {}).items() if isinstance(v, dict)}
    note = data.get("$extensions", {}).get("com.solidigm.brand", {}).get("preferReducedMotion", "")
    return {
        "status": "ok",
        "durations": durations,
        "easings": easings,
        "transforms": transforms,
        "reduced_motion_note": note,
        "tokens": data,
    }


def get_icon(name: str) -> Dict[str, Any]:
    """Look up a Solidigm UI atom icon by name.

    Parameters
    ----------
    name : str
        Icon name — e.g. ``"arrowDouble"``, ``"arrow-double"``,
        ``"chevronDown"``, ``"chevron-down"``.
        Partial names (e.g. ``"arrow"``) fuzzy-match available icons.
    """
    data = _read_json(os.path.join(config.tokens_dir, "icons.json"))
    atoms = data.get("icon", {}).get("atom", {})
    # Normalize: strip hyphens and lowercase for fuzzy key match
    needle = "".join(ch for ch in name.lower() if ch.isalnum())
    # Exact match first
    for key, token in atoms.items():
        if "".join(ch for ch in key.lower() if ch.isalnum()) == needle:
            return {
                "status": "ok",
                "name": key,
                "token": token,
                "sizes": data.get("icon", {}).get("size", {}),
            }
    # Partial / fuzzy match
    for key, token in atoms.items():
        if needle in "".join(ch for ch in key.lower() if ch.isalnum()):
            return {
                "status": "ok",
                "name": key,
                "token": token,
                "sizes": data.get("icon", {}).get("size", {}),
                "fuzzy": True,
            }
    return {
        "status": "not_found",
        "name": name,
        "available": list(atoms.keys()),
    }


def get_voice(trait: Optional[str] = None) -> Dict[str, Any]:
    """Return Solidigm brand voice tokens and copy guidelines.

    Parameters
    ----------
    trait : str, optional
        One of: ``optimistic``, ``analytical``, ``passionate``, ``genuine``,
        ``ambitious``. Omit for the full voice token set.
    """
    data = _read_json(os.path.join(config.tokens_dir, "voice.json"))
    if trait:
        t = data.get("voice", {}).get("traits", {}).get(trait.lower())
        if t is None:
            available = list(data.get("voice", {}).get("traits", {}).keys())
            return {"status": "not_found", "trait": trait, "available": available}
        return {"status": "ok", "trait": trait, "token": t}
    return {"status": "ok", "tokens": data}


def _normalize_color_key(s: str) -> str:
    """Normalize a color name for fuzzy matching: lowercase, no spaces/hyphens/underscores."""
    return "".join(ch for ch in s.lower() if ch.isalnum())


def get_color(name: str) -> Dict[str, Any]:
    """Look up a single brand color by name.

    Matching is case-insensitive and ignores spaces, hyphens, and underscores,
    so ``"Solidigm Purple"``, ``"solidigm-purple"``, and ``"solidigmpurple"``
    all resolve to the same token.
    """
    data = _read_json(os.path.join(config.tokens_dir, "colors.json"))
    needle = _normalize_color_key(name)
    matches: List[Dict[str, Any]] = []
    for group_name, group in data.items():
        if not isinstance(group, dict):
            continue
        for token_name, token in group.items():
            if not isinstance(token, dict):
                continue
            if _normalize_color_key(token_name) == needle:
                return {
                    "status": "ok",
                    "name": token_name,
                    "group": group_name,
                    "hex": token.get("$value"),
                    "type": token.get("$type"),
                }
            if needle in _normalize_color_key(token_name):
                matches.append(
                    {
                        "name": token_name,
                        "group": group_name,
                        "hex": token.get("$value"),
                    }
                )
    if matches:
        return {"status": "ambiguous", "query": name, "matches": matches}
    return {"status": "not_found", "name": name}


def get_brand_guidelines(topic: Optional[str] = None) -> Dict[str, Any]:
    """Return the brand guidelines markdown (full or a single topic section)."""
    # Prefer brand/brand.md (canonical); fall back to docs/brand-guidelines.md (legacy)
    candidates = [
        os.path.join(config.brand_dir, "brand.md"),
        os.path.join(config.docs_dir, "brand-guidelines.md"),
    ]
    path = next((p for p in candidates if os.path.isfile(p)), None)
    if path is None:
        return {"status": "error", "error": "brand guidelines file not found"}

    text = _read_text(path)
    if not topic:
        return {"status": "ok", "content": text}

    # Naive section extraction: look for a heading containing the topic
    needle = topic.strip().lower()
    lines = text.splitlines()
    capture = False
    captured: List[str] = []
    current_level = 0
    for line in lines:
        stripped = line.lstrip("#").strip().lower()
        level = len(line) - len(line.lstrip("#"))
        if level > 0 and needle in stripped:
            capture = True
            current_level = level
            captured = [line]
            continue
        if capture:
            if level and 0 < level <= current_level and needle not in stripped:
                break
            captured.append(line)
    if captured:
        return {"status": "ok", "topic": topic, "content": "\n".join(captured)}
    return {"status": "not_found", "topic": topic}


# ---------------------------------------------------------------------------
# Asset tools
# ---------------------------------------------------------------------------
async def list_assets(
    category: Optional[str] = None,
    include_sharepoint: bool = True,
) -> Dict[str, Any]:
    """List all brand assets.

    Merges local repo assets with SharePoint results when configured.
    ``category`` ∈ {logo, illustration, icon, image, template, product-render, doc} or omit for all.
    """
    return await assets_mod.list_all_assets(
        category=category, include_sharepoint=include_sharepoint
    )


async def get_asset(
    name: Optional[str] = None,
    path: Optional[str] = None,
    category: Optional[str] = None,
) -> Dict[str, Any]:
    """Retrieve a single brand asset by name or path.

    Pass ``name`` (substring) to fuzzy-match, or ``path`` (exact rel_path from
    ``list_assets``) for a precise lookup.  Optionally narrow with ``category``.
    Returns the asset record including ``download_url`` (SharePoint pre-auth,
    ~1 hr TTL) or ``url`` (local public path).
    """
    return await assets_mod.get_asset(name=name, path=path, category=category)


def get_logo(
    variant: str = "standard",
    color: str = "purple",
    resolution: Optional[str] = None,
    fmt: str = "png",
) -> Dict[str, Any]:
    """Resolve a specific logo file from the local manifest.

    Parameters
    ----------
    variant : ``s-mark`` | ``standard`` | ``stacked`` | ``wordmark``
    color : ``black`` | ``purple`` | ``blue`` | ``white``
    resolution : e.g. ``1920x1080``, ``3840x2160``, ``5760x3240``. Omit for SVG/EPS.
    fmt : ``png`` | ``svg`` | ``eps``
    """
    manifest = assets_mod.list_local_assets()
    fmt_l = fmt.lower()
    candidates = [
        a
        for a in manifest
        if a.get("category") == "logo"
        and a.get("variant") == variant
        and a.get("color") == color
        and a.get("format") == fmt_l
    ]
    if resolution and fmt_l not in ("svg", "eps"):
        candidates = [a for a in candidates if a.get("resolution") == resolution]
    if not candidates:
        return {
            "status": "not_found",
            "query": {"variant": variant, "color": color, "resolution": resolution, "format": fmt},
        }
    # Prefer the highest-resolution exact match if none specified
    candidates.sort(key=lambda a: a.get("size_bytes", 0), reverse=True)
    top = candidates[0]
    return {"status": "ok", "match": top, "alternatives": len(candidates) - 1}


async def search_brand_source_documents(
    folder: str = "",
    name_filter: str = "",
    user_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Recursively list files in the SharePoint brand library.

    Returns ``authorize_url`` instead of data when the caller isn't yet
    authenticated and SharePoint app-level access is not configured.
    """
    if not config.is_brand_sharepoint_configured:
        return {"status": "not_configured", "items": [], "count": 0}

    if user_id and not m365_oauth.is_user_authenticated(user_id):
        return {
            "status": "authentication_required",
            "authorize_url": m365_oauth.build_authorize_url(user_id),
        }

    result = await assets_mod.list_sharepoint_assets(folder=folder, user_id=user_id)
    if name_filter:
        needle = name_filter.lower()
        result["items"] = [i for i in result["items"] if needle in i.get("name", "").lower()]
        result["count"] = len(result["items"])
    return result


# ---------------------------------------------------------------------------
# UI toolkit tool
# ---------------------------------------------------------------------------
def get_ui_toolkit_class(name: str) -> Dict[str, Any]:
    """Return the CSS body of a toolkit class from the UI toolkit stylesheet."""
    # Search in order: dist/ (build output), site/public/ (deployed), docs/ (legacy)
    candidates = [
        os.path.join(config.REPO_ROOT, "dist", "ui-toolkit.min.css"),
        os.path.join(config.REPO_ROOT, "site", "public", "ui-toolkit.min.css"),
        os.path.join(config.docs_dir, "ui-toolkit.min.css"),
    ]
    path = next((p for p in candidates if os.path.isfile(p)), None)
    if path is None:
        return {"status": "error", "error": "ui-toolkit.min.css not found"}

    css = _read_text(path)
    needle = name if name.startswith(".") else f".{name}"
    matches: List[str] = []
    i = 0
    while True:
        idx = css.find(needle, i)
        if idx == -1:
            break
        # Ensure this is a class selector start (followed by { or , or space or :)
        end_char = css[idx + len(needle): idx + len(needle) + 1]
        if end_char in "{,: \n.":
            # Find enclosing rule
            brace_open = css.find("{", idx)
            brace_close = css.find("}", brace_open)
            if brace_open != -1 and brace_close != -1:
                matches.append(css[idx:brace_close + 1].strip())
        i = idx + len(needle)

    if not matches:
        return {"status": "not_found", "class": name}
    return {"status": "ok", "class": name, "rules": matches[:5], "total_matches": len(matches)}


# ---------------------------------------------------------------------------
# Brand context / prompt / validation tools
# ---------------------------------------------------------------------------
def get_brand_context(
    platform: Optional[str] = None,
    task: Optional[str] = None,
) -> Dict[str, Any]:
    """Return curated brand guidelines scoped to a platform and task.

    Parameters
    ----------
    platform : str, optional
        ``"marketing"``, ``"web-nextjs"``, ``"web-react"``, etc.
    task : str, optional
        ``"ui"``, ``"copy"``, ``"design"``, ``"review"``, ``"chart"``.
    """
    return context_mod.assemble(platform=platform, task=task)


def validate_brand_output(
    content: str,
    platform: Optional[str] = None,
) -> Dict[str, Any]:
    """Validate AI-generated content against brand quality gates.

    Returns ``{status: "pass"}`` when no errors are found, or
    ``{status: "fail", errors: [...], warnings: [...]}`` with details.
    """
    return validation_mod.validate(content, platform=platform)


def get_brand_system_prompt(
    platform: Optional[str] = None,
    include_design_rules: bool = True,
) -> Dict[str, Any]:
    """Return a pre-built brand-aware LLM system prompt.

    Inject this into the system message of any LLM conversation to ensure
    brand-compliant output.
    """
    return prompts_mod.build_system_prompt(
        platform=platform, include_design_rules=include_design_rules
    )
