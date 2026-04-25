# Solidigm Brand Context — Project Guidelines

This repo is the canonical source of truth for the Solidigm design system: tokens, UI toolkit, brand assets, guidelines, an Astro documentation site, and an MCP server that unifies all of the above for AI agents.

> **Cross-vendor agents:** see [`AGENTS.md`](../AGENTS.md) at the repo root for
> the same contract in agent-tool-agnostic form (Claude, Cursor, Aider, etc.).

## Ground rules for ALL brand content

Whenever a task involves Solidigm colors, typography, logos, trademarks, voice/tone, illustrations, or brand-compliant copy:

1. **Call the `solidigm-brand` MCP tools first.** Do not hallucinate hex values, font names, or trademark symbols. The canonical values live in `brand/` and are exposed through MCP.
2. **Validate generated UI / copy** with `validate_brand_output` before presenting final output.
3. **Use `get_brand_system_prompt`** when authoring new AI flows that produce brand-facing content — it returns a pre-built system prompt with current rules baked in.

## MCP tools (server: `solidigm-brand`, `http://localhost:8080`)

| Tool | Use when |
|------|----------|
| `get_design_tokens` | Need the full palette, typography scale, or W3C DTCG tokens |
| `get_color` | Looking up a single named color (fuzzy-matches `"solidigm-purple"`, `"Electric Teal"`, etc.) |
| `get_brand_guidelines` | Need narrative guidance on a topic (voice, logo, typography, etc.) |
| `get_ui_toolkit_class` | Implementing UI — look up a `tk-*` CSS class |
| `list_assets` | Need a logo, illustration, or doc — local + SharePoint unified manifest |
| `get_logo` | Resolving a specific logo variant/color/format |
| `search_brand_source_documents` | Need the official brand PDF, PPT, or source from SharePoint |
| `get_brand_context` | Assembling a prompt for an AI flow — scope by `platform` + `task` |
| `get_brand_system_prompt` | Need a drop-in system prompt for a brand-aware LLM call |
| `validate_brand_output` | Verifying AI-generated copy/markup passes brand quality gates |

## Code conventions

- **Python MCP server** lives in `brand_mcp/`. Requires Python 3.10+; use `brand_mcp/.venv`.
- **Astro site** lives in `site/`. Run from that directory (`npm run dev`, `npm run build`).
- **Canonical brand data** lives in `brand/` — never duplicate hex/font values elsewhere; read them via MCP or import from `@solidigm/brand-tokens`.
- **Tokens** are W3C DTCG JSON under `tokens/`. Changes there flow to the NPM package (`build.js`) and to Figma (`figma/tokens.json`).
- **Platform overrides** live in `brand/platforms/*.md` — add a new file when onboarding a new surface (iOS, Android, etc.).

## Build & test

```bash
# MCP server
cd brand_mcp && source .venv/bin/activate && python -m brand_mcp.server

# Astro site
cd site && npm run dev

# Token package
npm run build
```

CI: `.github/workflows/mcp-smoke-test.yml` runs on PR — 10 tool assertions + `/api/health` probe.

## Related docs

- [System architecture](../docs/architecture.md) — mermaid diagrams of the full stack
- [Roadmap](../docs/roadmap.md) — phases + open work
- [Brand MCP README](../brand_mcp/README.md) — operator-focused details
- [Brand foundation](../brand/brand.md) — voice, values, personality (canonical)
- [Quality gates](../brand/quality-gates.yaml) — 16 automated checks
