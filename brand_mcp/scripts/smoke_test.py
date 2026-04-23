#!/usr/bin/env python3
"""Smoke test — verifies SharePoint access via client credentials.

Usage::

    cd brand_mcp
    pip install -r requirements.txt
    python scripts/smoke_test.py

Requires M365_* and BRAND_SHAREPOINT_* values in ``brand_mcp/.env``.
"""
from __future__ import annotations

import asyncio
import sys

# Allow running from brand_mcp/scripts/ without installation
sys.path.insert(0, ".")

from brand_mcp.composer import assets  # noqa: E402
from brand_mcp.config import config  # noqa: E402


async def main() -> int:
    print(f"M365 configured:       {config.is_m365_configured}")
    print(f"SharePoint configured: {config.is_brand_sharepoint_configured}")
    print()
    print("--- Local assets ---")
    local = assets.list_local_assets()
    print(f"Found {len(local)} local assets")
    for a in local[:5]:
        print(f"  [{a['category']}] {a['rel_path']}")

    if config.is_brand_sharepoint_configured:
        print()
        print("--- SharePoint (app-level auth) ---")
        result = await assets.list_sharepoint_assets()
        print(f"status={result['status']} count={result.get('count')}")
        for item in result.get("items", [])[:5]:
            print(f"  {item.get('name')}")
    else:
        print()
        print("Skipping SharePoint check (not configured).")

    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
