"""Brand quality-gate validation.

Reads ``brand/quality-gates.yaml`` and runs lightweight checks against
content submitted by AI agents. This is not a pixel-perfect design linter —
it catches the most common brand violations that LLMs produce (wrong hex,
uppercase headlines, missing trademark symbol, etc.).
"""
from __future__ import annotations

import os
import re
from typing import Any, Dict, List, Optional

import yaml  # type: ignore[import-untyped]

from ..config import config
from . import colors as colors_mod

_gates: Optional[List[Dict[str, Any]]] = None


def _load_gates() -> List[Dict[str, Any]]:
    global _gates
    if _gates is not None:
        return _gates
    path = os.path.join(config.brand_dir, "quality-gates.yaml")
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    _gates = data.get("gates", [])
    return _gates


# ── Individual check functions ───────────────────────────────────

_HEX_RE = re.compile(r"#([0-9a-fA-F]{3,8})\b")


def _check_hex_in_palette(content: str) -> List[Dict[str, str]]:
    """Flag any hex color not in the approved palette."""
    palette = colors_mod.all_hex_values()
    issues: List[Dict[str, str]] = []
    for m in _HEX_RE.finditer(content):
        raw = m.group(0).lower()
        # Normalize 3-digit shorthand to 6-digit
        if len(raw) == 4:
            raw = f"#{raw[1]*2}{raw[2]*2}{raw[3]*2}"
        if raw not in palette:
            issues.append({"check": "hex_in_palette", "value": m.group(0), "message": f"{m.group(0)} is not in the approved Solidigm color palette"})
    return issues


def _check_no_uppercase_headings(content: str) -> List[Dict[str, str]]:
    """Flag markdown headings that are entirely uppercase."""
    issues: List[Dict[str, str]] = []
    for line in content.splitlines():
        stripped = line.lstrip("#").strip()
        if line.startswith("#") and stripped and stripped == stripped.upper() and stripped != stripped.lower():
            issues.append({"check": "no_uppercase_headings", "value": stripped, "message": f"Heading '{stripped}' is all uppercase — use title case or sentence case"})
    return issues


def _check_trademark(content: str) -> List[Dict[str, str]]:
    """Flag ® or © used with Solidigm."""
    issues: List[Dict[str, str]] = []
    if re.search(r"Solidigm®", content):
        issues.append({"check": "no_registered", "value": "Solidigm®", "message": "Use ™ not ® — Solidigm is not yet a registered trademark"})
    if re.search(r"©\s*Solidigm|Solidigm\s*©", content):
        issues.append({"check": "no_copyright", "value": "© Solidigm", "message": "Never use © in association with the Solidigm name or logo"})
    return issues


def _check_font_family(content: str) -> List[Dict[str, str]]:
    """Flag font-family declarations that use non-approved fonts."""
    allowed_normalized = {"sora", "notosans", "notosanssc", "notosanstc", "notosansjp", "notosanskr", "avenirnextltpro"}
    issues: List[Dict[str, str]] = []
    for m in re.finditer(r'font-family\s*:\s*([^;}\n]+)', content, re.IGNORECASE):
        families = [f.strip().strip("'\"") for f in m.group(1).split(",")]
        for fam in families:
            norm = "".join(ch for ch in fam.lower() if ch.isalnum())
            # Skip generic families and system stacks
            if norm in {"serif", "sansserif", "monospace", "cursive", "fantasy", "inherit", "initial", "unset",
                         "applesystem", "blinkmacsystemfont", "segoeui", "roboto", "helvetica", "arial"}:
                continue
            if norm and norm not in allowed_normalized:
                issues.append({"check": "font_allowlist", "value": fam, "message": f"Font '{fam}' is not in the approved typeface list (Sora, Noto Sans, Avenir Next LT Pro)"})
    return issues


def _check_accent_usage(content: str) -> List[Dict[str, str]]:
    """Warn if accent hex colors appear more than a few times (possible dominant use)."""
    accent_hexes = {"#00ffec", "#ea11bc", "#ffa42c"}
    issues: List[Dict[str, str]] = []
    for hex_val in accent_hexes:
        count = content.lower().count(hex_val)
        if count > 3:
            issues.append({"check": "accent_usage", "value": hex_val, "message": f"Accent color {hex_val} appears {count} times — accent colors should not be dominant"})
    return issues


def _check_spacing_grid(content: str) -> List[Dict[str, str]]:
    """Flag pixel spacing values that are not on the 4px grid.

    Checks padding/margin/gap/top/bottom/left/right declarations.
    Approved off-grid values (0, 100px, 120px, 150px) are explicitly allowed.
    """
    # Grid: multiples of 4px. Also allow 0 and the large section-spacing values.
    _OFF_GRID_EXEMPT = {0, 100, 120, 150}
    issues: List[Dict[str, str]] = []
    # Match px values in spacing-related CSS properties
    prop_re = re.compile(
        r'(?:padding|margin|gap|top|bottom|left|right|column-gap|row-gap|inset)'
        r'(?:-\w+)?\s*:\s*([^;}\n]+)',
        re.IGNORECASE,
    )
    px_re = re.compile(r'(\d+)px')
    for prop_match in prop_re.finditer(content):
        val_str = prop_match.group(1)
        for px_match in px_re.finditer(val_str):
            px_val = int(px_match.group(1))
            if px_val in _OFF_GRID_EXEMPT:
                continue
            if px_val % 4 != 0:
                issues.append({
                    "check": "spacing_grid",
                    "value": f"{px_val}px",
                    "message": (
                        f"{px_val}px is not on the 4px grid. "
                        "Use a value that is a multiple of 4 or a brand spacing token."
                    ),
                })
    return issues


def _check_motion_durations(content: str) -> List[Dict[str, str]]:
    """Flag transition/animation durations not in the approved set.

    Approved: 100ms, 200ms, 300ms, 500ms, 800ms.
    """
    _APPROVED_MS = {100, 200, 300, 500, 800}
    issues: List[Dict[str, str]] = []
    # Match transition/animation duration values in ms
    duration_re = re.compile(
        r'(?:transition|animation)(?:-duration)?\s*:[^;}\n]*?(\d+)ms',
        re.IGNORECASE,
    )
    for m in duration_re.finditer(content):
        ms = int(m.group(1))
        if ms not in _APPROVED_MS:
            issues.append({
                "check": "motion_durations",
                "value": f"{ms}ms",
                "message": (
                    f"{ms}ms is not an approved Solidigm motion duration. "
                    f"Use one of: {sorted(_APPROVED_MS)} (ms)."
                ),
            })
    return issues


def _check_border_radius(content: str) -> List[Dict[str, str]]:
    """Flag border-radius values not in the approved token set.

    Approved: 0px (brand default), 4px (sm), 8px (md), 16px (lg), 9999px (pill), 50%.
    """
    _APPROVED_PX = {0, 4, 8, 16, 9999}
    issues: List[Dict[str, str]] = []
    br_re = re.compile(r'border-radius\s*:\s*([^;}\n]+)', re.IGNORECASE)
    px_re = re.compile(r'(\d+)px')
    pct_re = re.compile(r'(\d+)%')
    for prop_match in br_re.finditer(content):
        val_str = prop_match.group(1).strip()
        # Allow CSS variables and 50%
        if 'var(' in val_str:
            continue
        pct_vals = [int(m.group(1)) for m in pct_re.finditer(val_str)]
        if pct_vals and all(v == 50 for v in pct_vals):
            continue
        for px_match in px_re.finditer(val_str):
            px_val = int(px_match.group(1))
            if px_val not in _APPROVED_PX:
                issues.append({
                    "check": "border_radius",
                    "value": f"{px_val}px",
                    "message": (
                        f"border-radius {px_val}px is not an approved Solidigm value. "
                        "Use 0 (default), 4px, 8px, 16px, 9999px, or 50%."
                    ),
                })
    return issues


# Registry of automated checks
_CHECKS = {
    "hex_in_palette": _check_hex_in_palette,
    "no_uppercase_headings": _check_no_uppercase_headings,
    "trademark_mark": _check_trademark,
    "no_registered": _check_trademark,
    "font_allowlist": _check_font_family,
    "accent_usage": _check_accent_usage,
    "spacing_grid": _check_spacing_grid,
    "motion_durations": _check_motion_durations,
    "border_radius": _check_border_radius,
}


def validate(content: str, *, platform: Optional[str] = None) -> Dict[str, Any]:
    """Validate content against brand quality gates.

    Parameters
    ----------
    content : str
        The text/code/markup to validate.
    platform : str, optional
        Platform key for context (currently informational).

    Returns
    -------
    dict with ``status`` (``"pass"`` or ``"fail"``), ``errors``, ``warnings``,
    and the full ``issues`` list.
    """
    gates = _load_gates()
    all_issues: List[Dict[str, Any]] = []

    # Run each automated check that has an implementation
    seen_checks: set[str] = set()
    for gate in gates:
        check_name = gate.get("check", "")
        if check_name in seen_checks:
            continue
        seen_checks.add(check_name)
        fn = _CHECKS.get(check_name)
        if fn is None:
            continue
        for issue in fn(content):
            all_issues.append({
                **issue,
                "gate_id": gate.get("id"),
                "severity": gate.get("severity", "warning"),
                "description": gate.get("description"),
            })

    errors = [i for i in all_issues if i["severity"] == "error"]
    warnings = [i for i in all_issues if i["severity"] == "warning"]

    return {
        "status": "fail" if errors else "pass",
        "platform": platform,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "gate_count": len(gates),
    }
