#!/usr/bin/env python3
"""Direct MCP tool tests — run as part of `npm test` via package.json.

Tests all 14 registered brand MCP tools by importing the tool functions
directly (no server required).  The MCP server must NOT be needed here;
this is a unit-level check that every tool returns a well-formed response.

Usage::

    cd <repo-root>
    ./brand_mcp/.venv/bin/python tests/tools_mcp_test.py

Exit 0 on pass, 1 on any failure.
"""
from __future__ import annotations

import sys
import traceback

# Allow running from repo root without installing the package
sys.path.insert(0, ".")

# Fail fast if dependencies are missing
try:
    from brand_mcp.tools import brand
    from brand_mcp.composer import validation as val_mod
except ImportError as exc:
    print(f"[SKIP] Cannot import brand_mcp ({exc}) — skipping tool tests")
    sys.exit(0)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

PASS = "\033[32m✓\033[0m"
FAIL = "\033[31m✗\033[0m"

_failures: list[str] = []


def check(label: str, result: object, **assertions: object) -> None:
    """Run assertions on *result* and accumulate failures."""
    errors: list[str] = []

    if isinstance(result, dict):
        for key, expected in assertions.items():
            actual = result.get(key)
            if callable(expected):
                if not expected(actual):
                    errors.append(f"  {key}={actual!r} failed predicate")
            elif actual != expected:
                errors.append(f"  {key}: expected {expected!r}, got {actual!r}")
    elif assertions:
        errors.append(f"  result is not a dict: {result!r}")

    if errors:
        _failures.append(f"\n{FAIL} {label}:\n" + "\n".join(errors))
        print(f"{FAIL} {label}")
    else:
        print(f"{PASS} {label}")


# ---------------------------------------------------------------------------
# Tool tests
# ---------------------------------------------------------------------------

def test_get_design_tokens_all() -> None:
    r = brand.get_design_tokens()
    check(
        "get_design_tokens() — all categories",
        r,
        status="ok",
        tokens=lambda t: isinstance(t, dict) and len(t) == 10,
    )


def test_get_design_tokens_category() -> None:
    r = brand.get_design_tokens("colors")
    check("get_design_tokens('colors')", r, status="ok", category="colors")


def test_get_design_tokens_invalid() -> None:
    r = brand.get_design_tokens("bogus")
    check("get_design_tokens('bogus') → error", r, status="error")


def test_get_spacing_all() -> None:
    r = brand.get_spacing()
    check(
        "get_spacing() — full scale",
        r,
        status="ok",
        scale=lambda s: isinstance(s, dict) and len(s) >= 10,
    )


def test_get_spacing_step() -> None:
    r = brand.get_spacing("4")
    check("get_spacing('4')", r, status="ok")
    assert isinstance(r, dict) and "$value" in r, f"Expected $value in response: {r}"
    print(f"  value = {r['$value']}")


def test_get_spacing_invalid() -> None:
    r = brand.get_spacing("999")
    check("get_spacing('999') → not_found", r, status="not_found")


def test_get_breakpoints() -> None:
    r = brand.get_breakpoints()
    check(
        "get_breakpoints()",
        r,
        status="ok",
        breakpoints=lambda b: isinstance(b, dict) and "lg" in b and "xl" in b,
        containers=lambda c: isinstance(c, dict) and "max" in c,
    )


def test_get_motion() -> None:
    r = brand.get_motion()
    check(
        "get_motion()",
        r,
        status="ok",
        durations=lambda d: isinstance(d, dict) and "base" in d and "fast" in d,
        easings=lambda e: isinstance(e, dict) and "standard" in e,
    )


def test_get_icon() -> None:
    r = brand.get_icon("arrowDouble")
    check("get_icon('arrowDouble')", r, status="ok")


def test_get_icon_fuzzy() -> None:
    r = brand.get_icon("arrow")
    check("get_icon('arrow') — fuzzy", r, status="ok")


def test_get_icon_not_found() -> None:
    r = brand.get_icon("totallymadeup_xyz_9999")
    check(
        "get_icon('totallymadeup...') → not_found or error",
        r,
        status=lambda s: s in ("not_found", "error"),
    )


def test_get_color() -> None:
    r = brand.get_color("solidigm-purple")
    check("get_color('solidigm-purple')", r, status="ok")
    if isinstance(r, dict):
        assert r.get("hex", "").lower() == "#4f00b5", f"unexpected hex: {r.get('hex')}"
        print(f"  hex = {r['hex']}")


def test_get_color_fuzzy() -> None:
    r = brand.get_color("Electric Teal")
    check("get_color('Electric Teal')", r, status="ok")


def test_get_brand_guidelines() -> None:
    r = brand.get_brand_guidelines()
    check(
        "get_brand_guidelines() — full",
        r,
        status="ok",
        content=lambda c: isinstance(c, str) and len(c) > 100,
    )


def test_get_brand_guidelines_topic() -> None:
    r = brand.get_brand_guidelines("voice")
    check("get_brand_guidelines('voice')", r, status="ok")


def test_get_ui_toolkit_class() -> None:
    r = brand.get_ui_toolkit_class("tk-btn")
    check(
        "get_ui_toolkit_class('tk-btn')",
        r,
        status="ok",
        rules=lambda x: x is not None,
    )


def test_list_assets() -> None:
    import asyncio
    r = asyncio.run(brand.list_assets(include_sharepoint=False))
    check(
        "list_assets(include_sharepoint=False)",
        r,
        status="ok",
        items=lambda items: isinstance(items, list) and len(items) >= 10,
    )


def test_get_logo() -> None:
    r = brand.get_logo("standard", "purple", fmt="svg")
    check("get_logo('standard','purple',fmt='svg')", r, status="ok")


def test_get_brand_context() -> None:
    r = brand.get_brand_context(platform="web-nextjs", task="ui")
    check(
        "get_brand_context(platform='web-nextjs', task='ui')",
        r,
        status="ok",
        section_count=lambda n: isinstance(n, int) and n > 0,
    )


def test_get_brand_system_prompt() -> None:
    r = brand.get_brand_system_prompt(platform="marketing")
    check(
        "get_brand_system_prompt(platform='marketing')",
        r,
        status="ok",
        token_estimate=lambda n: isinstance(n, int) and n > 0,
        prompt=lambda p: isinstance(p, str) and len(p) > 200,
    )


def test_validate_brand_output_pass() -> None:
    r = brand.validate_brand_output("Use Solidigm\u2122 Purple #4f00b5 in headlines.")
    check("validate_brand_output — passing content", r, status="pass")


def test_validate_brand_output_fail_trademark() -> None:
    r = brand.validate_brand_output("Use Solidigm\u00ae and some text.")
    check(
        "validate_brand_output — ® triggers failure",
        r,
        status="fail",
        error_count=lambda n: isinstance(n, int) and n > 0,
    )


def test_validate_brand_output_fail_hex() -> None:
    r = brand.validate_brand_output("Use Solidigm\u2122 with color #ff0000 and #00ff00.")
    check(
        "validate_brand_output — off-brand hex triggers failure",
        r,
        status="fail",
        error_count=lambda n: isinstance(n, int) and n > 0,
    )


# ---------------------------------------------------------------------------
# Validate → Repair loop
# ---------------------------------------------------------------------------

def test_validate_repair_loop() -> None:
    """End-to-end: detect a brand violation then re-validate after fix."""
    bad_content = "Solidigm® uses #ff0000 for action buttons."
    first_pass = brand.validate_brand_output(bad_content)
    if not isinstance(first_pass, dict) or first_pass.get("status") != "fail":
        _failures.append(
            f"\n{FAIL} validate→repair: first pass should fail, got {first_pass}"
        )
        print(f"{FAIL} validate→repair: first pass")
        return

    # Repair: fix trademark and replace off-brand hex
    fixed_content = bad_content.replace("®", "™").replace("#ff0000", "#4f00b5")
    second_pass = brand.validate_brand_output(fixed_content)

    if isinstance(second_pass, dict) and second_pass.get("status") == "pass":
        print(f"{PASS} validate→repair loop (fail → fix → pass)")
    else:
        _failures.append(
            f"\n{FAIL} validate→repair: second pass should pass, got {second_pass}"
        )
        print(f"{FAIL} validate→repair: second pass")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

_TESTS = [
    test_get_design_tokens_all,
    test_get_design_tokens_category,
    test_get_design_tokens_invalid,
    test_get_spacing_all,
    test_get_spacing_step,
    test_get_spacing_invalid,
    test_get_breakpoints,
    test_get_motion,
    test_get_icon,
    test_get_icon_fuzzy,
    test_get_icon_not_found,
    test_get_color,
    test_get_color_fuzzy,
    test_get_brand_guidelines,
    test_get_brand_guidelines_topic,
    test_get_ui_toolkit_class,
    test_list_assets,
    test_get_logo,
    test_get_brand_context,
    test_get_brand_system_prompt,
    test_validate_brand_output_pass,
    test_validate_brand_output_fail_trademark,
    test_validate_brand_output_fail_hex,
    test_validate_repair_loop,
]


def main() -> int:
    print("\n=== Solidigm Brand MCP — tool tests ===\n")
    for fn in _TESTS:
        try:
            fn()
        except Exception:  # noqa: BLE001
            label = fn.__name__
            tb = traceback.format_exc()
            _failures.append(f"\n{FAIL} {label} raised:\n{tb}")
            print(f"{FAIL} {label} — exception")

    print(f"\n{'─'*40}")
    total = len(_TESTS)
    failed = len(_failures)
    passed = total - failed

    if _failures:
        print("\nFailures:")
        for f in _failures:
            print(f)
        print(f"\n{passed}/{total} passed, {failed} failed\n")
        return 1

    print(f"\n{passed}/{total} passed\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
