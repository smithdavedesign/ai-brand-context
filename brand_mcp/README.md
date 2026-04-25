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
├── server.py              ← FastMCP app, tool + resource + prompt + HTTP routes
├── config.py              ← env-backed Config
├── requirements.txt
├── .env.example
├── scripts/
│   └── smoke_test.py
├── utils/
│   ├── __init__.py
│   ├── m365_oauth.py      ← Graph API + OAuth (PKCE + client credentials)
│   └── telemetry.py       ← Opt-in JSONL tool-call telemetry (N3)
├── composer/
│   ├── __init__.py
│   ├── cache.py
│   └── assets.py          ← local + SharePoint asset discovery
├── telemetry/             ← (gitignored) JSONL files written when enabled
└── tools/
    ├── __init__.py
    └── brand.py           ← tool implementations
```

## Telemetry (opt-in)

The server can record one JSONL line per tool call. Useful for prioritizing
which tools, colors, and components are actually used — drives the **N3** play
in [`docs/strategic-report.md`](../docs/strategic-report.md).

**Disabled by default.** To enable, set `BRAND_MCP_TELEMETRY_ENABLED=1` in
`brand_mcp/.env` and restart the server.

### Data model

One event per line, written to `brand_mcp/telemetry/YYYY-MM-DD.jsonl`:

```json
{
  "ts":   "2026-04-25T17:00:00.000Z",
  "event": "tool_call",
  "name": "get_color",
  "ok":   true,
  "ms":   12,
  "meta": { "name": "Solidigm Purple" }
}
```

Field reference:

| Field   | Type    | Notes |
|---------|---------|-------|
| `ts`    | string  | ISO-8601 UTC, millisecond precision |
| `event` | string  | Always `tool_call` today; reserved for future event types |
| `name`  | string  | The tool name (e.g. `get_color`, `validate_brand_output`) |
| `ok`    | bool    | `true` on success; `false` if the tool raised — for `validate_brand_output`, `ok` reflects pass/fail of the brand gates, not exceptions |
| `ms`    | int     | Wall-clock duration in milliseconds (best effort) |
| `meta`  | object  | Small scalar arguments only — strings truncated to 64 chars; lists/dicts/content blobs are dropped to protect privacy and keep file size bounded |

### Retention

- **Rotation:** one file per UTC day, automatic.
- **Cleanup:** none built in. The aggregator only reads the last 30 days
  by default (`load_recent_events(days=30)`); older files can be deleted
  manually or via `find brand_mcp/telemetry -mtime +90 -delete` in cron.
- **Privacy:** data is local-only, never transmitted. Content blobs (e.g. the
  `content` argument to `validate_brand_output`) are never stored — only
  the byte length.
- **Disable / scrub:** unset `BRAND_MCP_TELEMETRY_ENABLED` and delete
  `brand_mcp/telemetry/`. The directory is `.gitignore`d.

### Aggregation API

`GET /api/stats?days=30` returns:

```json
{
  "enabled": true,
  "window_days": 30,
  "total_calls": 1240,
  "error_count": 7,
  "error_rate": 0.0056,
  "avg_latency_ms": 18,
  "top_tools": [{"name": "get_color", "calls": 412, "errors": 0}, ...],
  "top_colors": [{"name": "Solidigm Purple", "calls": 88}, ...]
}
```

The Astro site renders this at `/admin/stats` ([source](../site/src/pages/admin/stats.astro)).

## Security notes

- **Never commit `.env`** — it's in `.gitignore` but double-check.
- Client secrets should be rotated via Entra portal on any suspected exposure.
- In production, replace the in-process token store with Redis or similar.
- Run behind Solidigm VPN / Entra SSO at the ingress layer.
