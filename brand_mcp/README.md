# Solidigm Brand MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io) server that exposes
the entire Solidigm design system — tokens, guidelines, UI toolkit, local
brand assets, and SharePoint-hosted official brand documents — to AI agents
and the Astro documentation site.

## Features

- **Design tokens** — read `tokens/*.json` directly (no auth)
- **Brand guidelines** — serve `docs/brand-guidelines.md` by topic
- **UI toolkit** — look up rules for any `.tk-*` or `.u-*` class
- **Local assets** — walk `site/public/assets/` and expose a structured manifest
- **SharePoint** — read the official brand library via Microsoft Graph
- **Per-user OAuth** — Entra ID Authorization Code + PKCE for delegated access
- **Client-credentials fallback** — app-level access when per-user tokens aren't present
- **TTL cache** — SharePoint folder listings cached (default 1 hour)
- **Rate-limit aware** — retries 429s with `Retry-After` + exponential backoff
- **HTTP endpoints for the site** — `/api/assets`, `/api/health`

## Prerequisites

- Python 3.11+
- An Entra (Azure AD) app registration with:
  - Web platform, redirect URI `{SERVER_BASE_URL}/microsoft/callback`
  - Admin-consented delegated permissions: `Sites.Read.All`, `User.Read`, `offline_access`
  - (Optional) admin-consented application permission `Sites.Read.All` for client-credentials mode
  - A client secret
- The composite Graph IDs for your SharePoint site + drive (see below)

## Setup

```bash
cd brand_mcp
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# …fill in secrets in .env…
```

### Resolve SharePoint IDs

Using Graph Explorer or curl with a bearer token:

```bash
# Site ID
GET https://graph.microsoft.com/v1.0/sites/yourtenant.sharepoint.com:/sites/YourBrandSite
# → copy the composite "id" → BRAND_SHAREPOINT_SITE_ID

# Drive ID
GET https://graph.microsoft.com/v1.0/sites/{site-id}/drives
# → copy the "id" of the document library → BRAND_SHAREPOINT_DRIVE_ID
```

## Run

```bash
python -m brand_mcp.server
# → http://localhost:8080
# MCP endpoint: http://localhost:8080/mcp
# Health:       http://localhost:8080/api/health
```

## Smoke test

```bash
python scripts/smoke_test.py
```

## Tools exposed

| Tool | Description |
|------|-------------|
| `get_design_tokens` | All tokens, or filter by category (`colors`, `typography`) |
| `get_color` | Look up a single color by name |
| `get_brand_guidelines` | Full guidelines, or a specific topic section |
| `get_ui_toolkit_class` | Look up CSS rules for a toolkit class |
| `list_assets` | Unified list of local + SharePoint assets |
| `get_logo` | Resolve a specific logo variant/color/resolution |
| `search_brand_source_documents` | SharePoint-only — recursive brand library search |

## Resources exposed

| URI | Content |
|-----|---------|
| `brand://tokens/colors` | `tokens/colors.json` |
| `brand://tokens/typography` | `tokens/typography.json` |
| `brand://guidelines/main` | `docs/brand-guidelines.md` |
| `brand://toolkit/css` | `docs/ui-toolkit.min.css` |
| `brand://assets/manifest` | Walk of `site/public/assets/` with parsed metadata |

## Wire into an MCP client

Three transport options are available depending on the client:

- **HTTP** — server runs as a shared service (`http://host:8080/mcp`). Best for teams.
- **Stdio** — client spawns `python -m brand_mcp.server` locally. Best for solo dev, no shared server needed.

### VS Code (Copilot / Agent Mode)

See `.vscode/mcp.json` at the repo root. It ships with both an HTTP entry (`solidigm-brand`) and a stdio entry (`solidigm-brand-local`). Pick one and remove the other, or leave both and toggle in the MCP panel.

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

**HTTP transport** (requires `brand_mcp` deployed somewhere you can reach):

```json
{
  "mcpServers": {
    "solidigm-brand": {
      "type": "http",
      "url": "http://brand-mcp.internal.solidigm.com:8080/mcp"
    }
  }
}
```

**Stdio transport** (runs locally — requires the venv to be set up):

```json
{
  "mcpServers": {
    "solidigm-brand": {
      "command": "/absolute/path/to/ai-brand-context/brand_mcp/.venv/bin/python",
      "args": ["-m", "brand_mcp.server"],
      "cwd": "/absolute/path/to/ai-brand-context",
      "env": {
        "MCP_TRANSPORT": "stdio"
      }
    }
  }
}
```

> Restart Claude Desktop after editing. Verify by asking Claude: *"What MCP tools do you have available?"* — you should see `get_design_tokens`, `get_color`, `get_logo`, etc.

### Cursor

Same schema as Claude Desktop, written to `~/.cursor/mcp.json` (create the file if it doesn't exist).

### Anthropic Claude (web / API)

The web Claude client does not yet accept custom MCP servers directly. For agentic use against our server, use the Anthropic SDK with the [`claude-agent-sdk`](https://docs.claude.com/en/api/agent-sdk) and point it at our HTTP endpoint — or wrap the HTTP routes (`/api/assets`, `/api/health`) as plain REST for older integrations.

### Anthropic Claude Code CLI

```bash
claude mcp add --transport http solidigm-brand http://brand-mcp.internal.solidigm.com:8080/mcp
```

## Architecture

```
brand_mcp/
├── __init__.py
├── server.py              ← FastMCP app, tool + resource + HTTP routes
├── config.py              ← env-backed Config
├── requirements.txt
├── .env.example
├── scripts/
│   └── smoke_test.py
├── utils/
│   ├── __init__.py
│   └── m365_oauth.py      ← Graph API + OAuth (PKCE + client credentials)
├── composer/
│   ├── __init__.py
│   ├── cache.py
│   └── assets.py          ← local + SharePoint asset discovery
└── tools/
    ├── __init__.py
    └── brand.py           ← tool implementations
```

## Security notes

- **Never commit `.env`** — it's in `.gitignore` but double-check.
- Client secrets should be rotated via Entra portal on any suspected exposure.
- In production, replace the in-process token store with Redis or similar.
- Run behind Solidigm VPN / Entra SSO at the ingress layer.
