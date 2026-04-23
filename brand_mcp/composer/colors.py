"""Color palette lookup from ``brand/colors.json``.

Provides richer data than the raw design tokens — includes RGB values,
usage notes, group classification, and restriction flags. Used by the
``get_color`` MCP tool for enriched responses and by ``validation.py``
to check that colors are on-palette.
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

from ..config import config

_colors: Optional[Dict[str, Any]] = None


def _load() -> Dict[str, Any]:
    global _colors
    if _colors is not None:
        return _colors
    path = os.path.join(config.brand_dir, "colors.json")
    with open(path, "r", encoding="utf-8") as f:
        _colors = json.load(f)
    return _colors


def _normalize(s: str) -> str:
    return "".join(ch for ch in s.lower() if ch.isalnum())


def all_colors() -> List[Dict[str, Any]]:
    """Return a flat list of every color entry with its group category."""
    data = _load()
    result: List[Dict[str, Any]] = []
    for category, colors in data.items():
        for name, info in colors.items():
            result.append({"name": name, "category": category, **info})
    return result


def all_hex_values() -> set[str]:
    """Return the set of all approved hex values (lowercase)."""
    return {c["hex"].lower() for c in all_colors()}


def lookup(name: str) -> Dict[str, Any]:
    """Look up a color by name with fuzzy matching.

    Returns ``{status: "ok", ...}`` on exact match,
    ``{status: "ambiguous", matches: [...]}`` on partial match,
    or ``{status: "not_found"}`` if nothing matches.
    """
    data = _load()
    needle = _normalize(name)
    matches: List[Dict[str, Any]] = []

    for category, colors in data.items():
        for color_name, info in colors.items():
            norm = _normalize(color_name)
            if norm == needle:
                return {
                    "status": "ok",
                    "name": color_name,
                    "category": category,
                    **info,
                }
            if needle in norm:
                matches.append({"name": color_name, "category": category, **info})

    if matches:
        return {"status": "ambiguous", "query": name, "matches": matches}
    return {"status": "not_found", "query": name}
