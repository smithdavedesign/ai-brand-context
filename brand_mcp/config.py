"""Environment-backed configuration for the Solidigm Brand MCP server."""
from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load .env from the mcp/ directory (one level up from this file)
_ROOT = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_ROOT, ".env"))


def _opt(key: str, default: str = "") -> str:
    return os.getenv(key, default).strip()


def _int(key: str, default: int) -> int:
    raw = os.getenv(key)
    try:
        return int(raw) if raw else default
    except ValueError:
        return default


@dataclass(frozen=True)
class Config:
    # Entra / M365 app registration
    M365_TENANT_ID: str = _opt("M365_TENANT_ID")
    M365_CLIENT_ID: str = _opt("M365_CLIENT_ID")
    M365_CLIENT_SECRET: str = _opt("M365_CLIENT_SECRET")

    # SharePoint library
    BRAND_SHAREPOINT_SITE_ID: str = _opt("BRAND_SHAREPOINT_SITE_ID")
    BRAND_SHAREPOINT_DRIVE_ID: str = _opt("BRAND_SHAREPOINT_DRIVE_ID")
    BRAND_SHAREPOINT_CACHE_TTL: int = _int("BRAND_SHAREPOINT_CACHE_TTL", 3600)

    # Server runtime
    SERVER_BASE_URL: str = _opt("SERVER_BASE_URL", "http://localhost:8080")
    MCP_HOST: str = _opt("MCP_HOST", "0.0.0.0")
    MCP_PORT: int = _int("MCP_PORT", 8080)

    # Repo paths (used by tools that read local tokens/assets)
    REPO_ROOT: str = os.path.abspath(os.path.join(_ROOT, os.pardir))

    @property
    def is_m365_configured(self) -> bool:
        return bool(self.M365_TENANT_ID and self.M365_CLIENT_ID and self.M365_CLIENT_SECRET)

    @property
    def is_brand_sharepoint_configured(self) -> bool:
        return bool(
            self.is_m365_configured
            and self.BRAND_SHAREPOINT_SITE_ID
            and self.BRAND_SHAREPOINT_DRIVE_ID
        )

    @property
    def tokens_dir(self) -> str:
        return os.path.join(self.REPO_ROOT, "tokens")

    @property
    def assets_dir(self) -> str:
        return os.path.join(self.REPO_ROOT, "site", "public", "assets")

    @property
    def docs_dir(self) -> str:
        return os.path.join(self.REPO_ROOT, "docs")

    @property
    def brand_dir(self) -> str:
        return os.path.join(self.REPO_ROOT, "brand")


config = Config()
