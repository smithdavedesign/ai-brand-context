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


# Registry of automated checks
_CHECKS = {
    "hex_in_palette": _check_hex_in_palette,
    "no_uppercase_headings": _check_no_uppercase_headings,
    "trademark_mark": _check_trademark,
    "no_registered": _check_trademark,
    "font_allowlist": _check_font_family,
    "accent_usage": _check_accent_usage,
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
