# AGENTS.md — Solidigm Brand Context

> Cross-vendor agent contract. Read this **first** when working in this repo.
> If you only read one file, read this one.

This file follows the [`AGENTS.md`](https://agents.md) convention adopted by
Anthropic, OpenAI, and major OSS frameworks. It tells any AI agent
(Copilot, Claude, Cursor, Aider, etc.) the minimum it needs to be useful and
brand-safe in this codebase.

---

## 1. Repo identity

This repository is the **canonical source of truth** for the Solidigm design
system. Anything here that conflicts with another system (Storybook, a Figma
file, a Notion page) — **this repo wins**. Other surfaces are downstream.

Components:

- `tokens/` — W3C DTCG design tokens (color, typography). Source of truth for hex/font values.
- `brand/` — canonical brand content (voice, guidelines, quality gates, platform overrides).
- `brand_mcp/` — Python MCP server exposing the system to AI agents (10 tools, 5 resources, 4 prompts, 4 HTTP routes).
- `site/` — Astro documentation site that consumes the MCP server.
- `.github/` — Copilot instructions, prompts, and the `brand-compliance` Skill.

See [`docs/INDEX.md`](docs/INDEX.md) for the doc map and
[`docs/architecture.md`](docs/architecture.md) for system diagrams.

---

## 2. MCP server

A long-running process at **`http://localhost:8080`** named **`solidigm-brand`**.

Start it:

```bash
cd brand_mcp && source .venv/bin/activate && python -m brand_mcp.server
```

### Tools (use these instead of guessing values)

| Tool | When to call |
|------|--------------|
| `get_design_tokens` | Need the full palette, type scale, or W3C DTCG tokens |
| `get_color` | Looking up a single color (fuzzy: `"solidigm-purple"`, `"Electric Teal"`) |
| `get_brand_guidelines` | Need narrative guidance on a topic (voice, logo, typography…) |
| `get_ui_toolkit_class` | Implementing UI — look up a `tk-*` CSS class |
| `list_assets` | Need any logo, illustration, or doc — local + SharePoint |
| `get_asset` | Resolve one asset by name or path (returns `code_paths`) |
| `get_logo` | Resolve a specific logo variant/color/format |
| `search_brand_source_documents` | Need the official brand PDF/PPT from SharePoint |
| `get_brand_context` | Assembling a prompt for an AI flow — scope by `platform` + `task` |
| `get_brand_system_prompt` | Need a drop-in system prompt for a brand-aware LLM call |
| `validate_brand_output` | Verify generated copy/markup passes brand quality gates |

### Prompts (canonical workflows)

Pre-built workflows you can invoke by name:

- `brand_check` — validate a piece of content against quality gates
- `generate_brand_compliant_copy` — full composer flow (context → draft → validate)
- `audit_built_site` — run the brand-compliance Skill on built HTML
- `propose_color` — fuzzy-resolve a color description to a canonical token

### Resources

- `brand://tokens/colors`
- `brand://tokens/typography`
- `brand://guidelines/main`
- `brand://toolkit/css`
- `brand://assets/manifest`

---

## 3. Hard rules (no-go zones)

These are non-negotiable. The `validate_brand_output` tool enforces all of them.

- **Trademark:** use `Solidigm™` (not `®`, not bare `Solidigm`).
- **Color:** only hex values that match `tokens/colors.json`. No invented hexes.
- **Typography:** only `Sequel100`, `Roboto`, and `Roboto Mono` — never substitutes.
- **Voice:** title case for headlines (no ALL CAPS), no em-dash overuse, no marketing fluff.
- **Logos:** use `get_logo` to resolve; never crop, recolor, or reposition the
  logo outside its clear-space rules.
- **Assets:** never duplicate hex/font values inline — read them through the
  MCP tools or import from `@solidigm/brand-tokens`.
- **Archived docs (`docs/_archive/`):** read-only, historical. Edit
  `tokens/`, `brand/`, or `docs/{architecture,roadmap,strategic-report,design-system-integration}.md` instead.

---

## 4. Validation flow (run before merging)

For any change that touches brand-facing output:

1. **Draft** with the MCP tools (`get_brand_context`, `get_color`, etc.).
2. **Validate** — call `validate_brand_output(content, platform)`. Repair until it passes.
3. **Audit** the built site — `node .github/skills/brand-compliance/scripts/audit-pages.mjs`. Target grade ≥ B.
4. **Test** — `npm test` runs the Playwright suite (24 tests across MCP + Astro UI).

---

## 5. Build & test commands

```bash
# MCP server
cd brand_mcp && source .venv/bin/activate && python -m brand_mcp.server

# Astro site
cd site && npm run dev          # dev server
cd site && npm run build        # production build into site/dist

# Token package
npm run build                   # regenerates dist/css, dist/js, dist/scss

# Asset code-path index (run after adding new asset references)
npm run index:assets            # writes brand/asset-index.json

# Tests
npm test                        # full Playwright suite
npm run test:api                # MCP API only
npm run test:ui                 # Assets page only

# Brand audit
node .github/skills/brand-compliance/scripts/audit-pages.mjs
```

---

## 6. PR checklist

Before opening a PR that touches the brand system:

- [ ] No new hex/font values outside `tokens/`
- [ ] `validate_brand_output` passes for new copy/markup
- [ ] `npm run build` succeeds (token + Astro)
- [ ] `npm test` passes (24/24 green)
- [ ] If new assets added: `npm run index:assets` was run and `brand/asset-index.json` is committed
- [ ] If new tools/prompts added: smoke test workflow updated (`.github/workflows/mcp-smoke-test.yml`)
- [ ] Doc map updated: changes reflected in [`docs/INDEX.md`](docs/INDEX.md) or relevant live doc

---

## 7. Where to look first

| Need | Go here |
|------|---------|
| System overview | [`docs/architecture.md`](docs/architecture.md) |
| What's planned | [`docs/roadmap.md`](docs/roadmap.md) |
| Why we built it this way | [`docs/strategic-report.md`](docs/strategic-report.md) |
| Figma + Storybook integration | [`docs/design-system-integration.md`](docs/design-system-integration.md) |
| Operator details for the MCP | [`brand_mcp/README.md`](brand_mcp/README.md) |
| Current brand voice/values | [`brand/brand.md`](brand/brand.md) |
| Active quality gates | [`brand/quality-gates.yaml`](brand/quality-gates.yaml) |
