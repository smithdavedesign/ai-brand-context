"""Asset discovery.

Two sources:

1. **Local repo** — files organized under ``site/public/assets/`` (logos,
   illustrations, docs). Fast, no auth.

2. **SharePoint** — the official Solidigm brand library via Microsoft Graph.
   For long-tail marketing / legal / pre-release assets that aren't mirrored
   into the repo.

The ``list_all_assets`` function returns a unified manifest with one row per
asset, regardless of source.
"""
from __future__ import annotations

import asyncio
import logging
import os
from typing import Any, Dict, List, Optional
from urllib.parse import quote

from ..config import config
from ..utils import m365_oauth
from .cache import Cache

log = logging.getLogger(__name__)

# SharePoint root folder inside the drive (override in .env if needed)
_SHAREPOINT_BRAND_ROOT = "Files/Brand/Core Brand Assets/Updated Jan 2026"

# Asset category → folder-name hints (substring match, case-insensitive)
_ASSET_FOLDER_HINTS: Dict[str, List[str]] = {
    "logo": ["logo", "wordmark", "s mark", "s-mark"],
    "illustration": ["illustration", "icon", "component"],
    "doc": ["guideline", "trademark", "brand guideline"],
}

# SharePoint folder-name prefix → category (matched against any path segment, lowercase)
_SP_FOLDER_CATEGORIES: Dict[str, str] = {
    "02 - logos":                    "logo",
    "04 - presentation template":    "template",
    "05 - word doc template":        "template",
    "06 - email signature":          "template",
    "07 - teams backgrounds":        "template",
    "08 - excel template":           "template",
    "09 - icons":                    "icon",
    "10 - email header templates":   "template",
    "11 - images":                   "image",
    "12 - product renders":          "product-render",
    "01 - brand guidelines":         "doc",
}


def _infer_sp_category(rel_path: str) -> str:
    """Return a category string by matching any path segment against _SP_FOLDER_CATEGORIES."""
    lower = rel_path.lower()
    for folder_key, cat in _SP_FOLDER_CATEGORIES.items():
        if folder_key in lower:
            return cat
    return "other"

_cache = Cache(ttl_seconds=config.BRAND_SHAREPOINT_CACHE_TTL)

# ---------------------------------------------------------------------------
# Local asset manifest
# ---------------------------------------------------------------------------
_LOGO_COLORS = {"black", "purple", "blue", "white"}
_LOGO_VARIANTS = {"s-mark", "standard", "stacked", "wordmark"}


def _categorize_local(rel_path: str) -> str:
    parts = rel_path.split(os.sep)
    if parts and parts[0] == "logo":
        return "logo"
    if parts and parts[0] == "illustrations":
        return "illustration"
    if parts and parts[0] == "docs":
        return "doc"
    return "other"


def _parse_logo_meta(rel_path: str) -> Dict[str, Optional[str]]:
    """Extract {variant, color, resolution, format} from a logo file path."""
    parts = rel_path.split(os.sep)
    # Expected shape: logo/<variant>/<color>/<filename>
    variant = parts[1] if len(parts) > 1 and parts[1] in _LOGO_VARIANTS else None
    color = parts[2] if len(parts) > 2 and parts[2] in _LOGO_COLORS else None
    filename = parts[-1]
    ext = os.path.splitext(filename)[1].lstrip(".").lower() or None
    # Resolution pattern e.g. 1920x1080
    resolution: Optional[str] = None
    for token in filename.replace(".", "-").split("-"):
        if "x" in token and all(p.isdigit() for p in token.split("x")):
            resolution = token
            break
    return {
        "variant": variant,
        "color": color,
        "resolution": resolution,
        "format": ext,
    }


def list_local_assets() -> List[Dict[str, Any]]:
    """Walk ``site/public/assets/`` and return one record per file."""
    cached = _cache.get("local_manifest")
    if cached is not None:
        return cached  # type: ignore[return-value]

    assets: List[Dict[str, Any]] = []
    root = config.assets_dir
    if not os.path.isdir(root):
        log.warning("Local assets dir missing: %s", root)
        return assets

    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            if name.startswith("."):
                continue
            abs_path = os.path.join(dirpath, name)
            rel_path = os.path.relpath(abs_path, root)
            category = _categorize_local(rel_path)
            record: Dict[str, Any] = {
                "source": "local",
                "category": category,
                "name": name,
                "rel_path": rel_path,
                # Public URL when served by the Astro site
                "url": f"/assets/{rel_path.replace(os.sep, '/')}",
                "size_bytes": os.path.getsize(abs_path),
            }
            if category == "logo":
                record.update(_parse_logo_meta(rel_path))
            assets.append(record)

    _cache.set("local_manifest", assets)
    return assets


# ---------------------------------------------------------------------------
# SharePoint traversal (Graph API)
# ---------------------------------------------------------------------------
def _sanitize_folder_path(path: str) -> str:
    parts = [p for p in path.split("/") if p and p not in (".", "..") and ":" not in p]
    return "/".join(parts)


def _encode_path_for_graph(path: str) -> str:
    """Percent-encode each segment of a folder path for use in a Graph API drive URL.

    Segments are encoded individually so that path separators (``/``) are
    preserved, but characters like ``?``, ``#``, ``&``, ``%`` that would
    otherwise confuse URL parsers are safely escaped.
    """
    return "/".join(quote(seg, safe="") for seg in path.split("/"))


async def _list_drive_items(
    folder_path: str,
    *,
    user_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """List items in a single SharePoint folder (non-recursive)."""
    cache_key = f"sp:folder:{folder_path}"
    cached = _cache.get(cache_key)
    if cached is not None:
        return cached  # type: ignore[return-value]

    path = _sanitize_folder_path(folder_path)
    if path:
        encoded = _encode_path_for_graph(path)
        endpoint = (
            f"/drives/{config.BRAND_SHAREPOINT_DRIVE_ID}/root:/"
            f"{encoded}:/children"
        )
    else:
        endpoint = f"/drives/{config.BRAND_SHAREPOINT_DRIVE_ID}/root/children"

    all_items: List[Dict[str, Any]] = []
    params: Optional[Dict[str, Any]] = {"$top": 200}
    next_url: Optional[str] = None

    while True:
        if next_url:
            # Graph gives full URL on paging; strip the base and re-request
            response = await m365_oauth.graph_request(
                next_url.replace("https://graph.microsoft.com/v1.0", ""),
                user_id=user_id,
            )
            params = None
        else:
            response = await m365_oauth.graph_request(
                endpoint, user_id=user_id, params=params
            )
        all_items.extend(response.get("value", []))
        next_url = response.get("@odata.nextLink")
        if not next_url:
            break

    _cache.set(cache_key, all_items)
    return all_items


async def _list_drive_items_recursive(
    folder_path: str,
    *,
    user_id: Optional[str] = None,
    max_depth: int = 4,
) -> List[Dict[str, Any]]:
    """Recursively list files under a folder, capped at ``max_depth``."""
    results: List[Dict[str, Any]] = []

    async def walk(path: str, depth: int) -> None:
        if depth > max_depth:
            return
        items = await _list_drive_items(path, user_id=user_id)
        subfolders: List[str] = []
        for it in items:
            if "folder" in it:
                subfolders.append(f"{path}/{it['name']}" if path else it["name"])
            else:
                rel = f"{path}/{it.get('name')}" if path else it.get("name", "")
                results.append(
                    {
                        "source": "sharepoint",
                        "category": _infer_sp_category(rel),
                        "name": it.get("name"),
                        "rel_path": rel,
                        "url": it.get("webUrl"),
                        "download_url": it.get("@microsoft.graph.downloadUrl"),
                        "size_bytes": it.get("size"),
                    }
                )
        # Traverse subfolders in batches of 10
        for i in range(0, len(subfolders), 10):
            chunk = subfolders[i : i + 10]
            await asyncio.gather(*(walk(sub, depth + 1) for sub in chunk))

    await walk(_sanitize_folder_path(folder_path), 0)
    return results


async def list_sharepoint_assets(
    *,
    folder: str = "",
    user_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Return SharePoint brand assets under the configured root."""
    if not config.is_brand_sharepoint_configured:
        return {"status": "not_configured", "items": [], "count": 0}

    root = _SHAREPOINT_BRAND_ROOT
    full = f"{root}/{folder}" if folder else root
    try:
        items = await _list_drive_items_recursive(full, user_id=user_id)
    except Exception as exc:  # noqa: BLE001
        log.exception("SharePoint listing failed")
        return {"status": "error", "error": str(exc), "items": [], "count": 0}

    return {"status": "ok", "items": items, "count": len(items)}


# ---------------------------------------------------------------------------
# Unified manifest
# ---------------------------------------------------------------------------
async def get_asset(
    *,
    name: Optional[str] = None,
    path: Optional[str] = None,
    category: Optional[str] = None,
    user_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Return a single asset by name substring or exact rel_path.

    Searches the unified manifest (local + SharePoint).  The first matching
    item is returned together with its ``download_url`` (SharePoint pre-auth,
    valid ~1 hr) or ``url`` (local public path).
    """
    if not name and not path:
        return {"status": "error", "error": "Provide 'name' or 'path'"}

    manifest = await list_all_assets(category=category, user_id=user_id)
    items = manifest["items"]

    if path:
        needle_path = path.lower()
        matches = [a for a in items if (a.get("rel_path") or "").lower() == needle_path]
    else:
        needle_name = (name or "").lower()
        matches = [a for a in items if needle_name in (a.get("name") or "").lower()]

    if not matches:
        return {"status": "not_found", "query": {"name": name, "path": path, "category": category}}

    # Return the best match + total count of alternatives
    best = matches[0]
    return {
        "status": "ok",
        "asset": best,
        "alternatives": len(matches) - 1,
        "all_matches": matches if len(matches) > 1 else None,
    }


async def list_all_assets(
    *,
    category: Optional[str] = None,
    user_id: Optional[str] = None,
    include_sharepoint: bool = True,
) -> Dict[str, Any]:
    """Return a unified list of local + SharePoint assets, optionally filtered."""
    local = list_local_assets()

    sharepoint: List[Dict[str, Any]] = []
    sp_status = "skipped"
    if include_sharepoint and config.is_brand_sharepoint_configured:
        sp = await list_sharepoint_assets(user_id=user_id)
        sharepoint = sp["items"]
        sp_status = sp["status"]

    combined = local + sharepoint
    if category:
        cat = category.lower()
        combined = [a for a in combined if a.get("category", "").lower() == cat]

    return {
        "status": "ok",
        "sharepoint_status": sp_status,
        "count": len(combined),
        "local_count": sum(1 for a in combined if a.get("source") == "local"),
        "sharepoint_count": sum(1 for a in combined if a.get("source") == "sharepoint"),
        "items": combined,
    }
