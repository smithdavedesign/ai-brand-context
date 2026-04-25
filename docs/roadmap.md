# Roadmap — Solidigm Brand MCP + Asset Browser

Status key: `[x]` complete · `[~]` in progress · `[ ]` not started · `[!]` needs user action

---

## ✅ Phase 1 — Security triage

- [x] Expand `.gitignore` (`.env`, handoff doc, raw asset dumps, Python cruft)
- [x] Create `brand_mcp/.env.example` (safe template)
- [x] Verify handoff doc is not committed (`git log` confirmed clean)
- [!] **USER ACTION:** rotate the leaked `M365_CLIENT_SECRET` in Entra portal before deploying

---

## ✅ Phase 2 — MCP server scaffold

- [x] `mcp/requirements.txt` (httpx, fastmcp, cachetools, python-dotenv)
- [x] `mcp/config.py` — env-backed `Config` with path helpers
- [x] `mcp/utils/m365_oauth.py` — client-credentials + PKCE delegated flow + Graph client
- [x] `mcp/composer/cache.py` — TTL cache wrapper
- [x] `mcp/composer/assets.py` — local manifest walker + SharePoint recursive traversal
- [x] `mcp/server.py` — FastMCP app, tools, resources, HTTP routes
- [x] `brand_mcp/scripts/smoke_test.py` — local + SharePoint sanity check
- [x] `brand_mcp/README.md` — operator-focused docs

---

## ✅ Phase 3 — Best-in-class tools + resources

- [x] Tool: `get_design_tokens(category?)`
- [x] Tool: `get_color(name)`
- [x] Tool: `get_brand_guidelines(topic?)`
- [x] Tool: `get_ui_toolkit_class(name)`
- [x] Tool: `list_assets(category?, include_sharepoint?)`
- [x] Tool: `get_logo(variant, color, resolution?, fmt?)`
- [x] Tool: `search_brand_source_documents(folder, name_filter)` (SharePoint)
- [x] Resource: `brand://tokens/colors`
- [x] Resource: `brand://tokens/typography`
- [x] Resource: `brand://guidelines/main`
- [x] Resource: `brand://toolkit/css`
- [x] Resource: `brand://assets/manifest`

---

## ✅ Phase 4 — Astro `/assets` page

- [x] `site/src/pages/assets.astro` — filterable grid (category / color / variant / search)
- [x] Client fetches `${PUBLIC_MCP_URL}/api/assets`
- [x] Graceful offline message when MCP is unreachable
- [x] Nav + Footer + Layout updated for new route
- [x] `site/.env.example` with `PUBLIC_MCP_URL`
- [x] Per-asset preview modal with metadata + copy-URL
- [x] Paginate large result sets in the UI (24 per page)
- [ ] Future: swap client-side fetch for Astro SSR API route on Azure SWA (if we move off GitHub Pages)

---

## ✅ Phase 5 — Developer UX

- [x] `.vscode/mcp.json` — HTTP + stdio server entries for Copilot
- [x] Document Claude Desktop / Cursor / Claude Code CLI config in `brand_mcp/README.md`
- [x] CI smoke test workflow at `.github/workflows/mcp-smoke-test.yml` (syntax + imports + tool assertions + `/api/health` probe)

---

## ✅ Phase 6 — Documentation

- [x] Root `README.md` — add "MCP Server" section + updated repo structure
- [x] `docs/architecture.md` — mermaid system diagram + sequence flows
- [x] `docs/roadmap.md` — this file
- [x] `site/src/pages/usage.astro` — "For AI Agents" tab added last session
- [x] `site/src/pages/governance.astro` — MCP contribution flow added last session

---

## ✅ Phase 7 — Verification (this session)

- [x] Fixed package-name collision: `mcp/` → `brand_mcp/` (the official MCP SDK publishes a top-level `mcp` package that was being shadowed — the server couldn't start until this was renamed)
- [x] `get_color()` now matches fuzzy (handles `"solidigm-purple"`, `"Solidigm Purple"`, `"solidigmpurple"`) with ambiguous-match response
- [x] All 7 tools exercised locally against real repo data
- [x] Server boots on `http://localhost:8080`
- [x] `/api/health` + `/api/assets` verified (returns 87 local assets)

---

## ✅ Phase 7b — Brand Composer & Context System

- [x] Created `brand/` canonical content directory (11 topic markdown files split from `docs/brand-guidelines.md`)
- [x] `brand/colors.json` — enriched palette with hex, RGB, usage notes, WCAG hints, group and restricted flags
- [x] `brand/quality-gates.yaml` — 16 brand quality gate rules with severity and check types
- [x] `brand/platforms/` — platform-specific overrides for marketing, web-nextjs, web-react
- [x] `brand_mcp/composer/colors.py` — rich palette lookup with fuzzy matching
- [x] `brand_mcp/composer/context.py` — task/platform-scoped brand context assembler
- [x] `brand_mcp/composer/prompts.py` — LLM system prompt builder (~3k tokens default)
- [x] `brand_mcp/composer/validation.py` — quality gate checker (hex palette, trademark, fonts, accent limits, heading case)
- [x] Tool: `get_brand_context(platform?, task?)` — scoped brand context
- [x] Tool: `validate_brand_output(content, platform?)` — pass/fail quality gates
- [x] Tool: `get_brand_system_prompt(platform?, include_design_rules?)` — pre-built system prompt
- [x] All 10 tools registered and smoke tested locally
- [x] CI workflow updated for new modules and tool assertions

---

## ✅ Phase 8 — VS Code Copilot Skill (brand rules + MCP wiring)

- [x] `.github/copilot-instructions.md` — always-on rules for the whole repo
- [x] `.github/instructions/solidigm-brand.instructions.md` — scoped via `applyTo` glob over `.astro/.css/.md/.tsx` etc.
- [x] `.github/prompts/brand-check.prompt.md` — `/brand-check <target>` single-shot validator
- [x] `.github/skills/brand-compliance/SKILL.md` + `scripts/audit-pages.mjs` — full site audit workflow
- [x] New HTTP route `POST /api/validate` on the MCP server (wraps `validate_brand_output`)
- [x] First full site audit executed — **site grade B** (11/16 pages A+); report at `docs/brand-audit-2026-04-23.md`
- [x] README + architecture diagram refreshed to show the Skill layer
- [x] `sharepoint-mcp-handoff/` removed (twins verified)

---

## 🚧 Phase 9 — Now plays from the strategic report

Tracks the **N1–N5** moves identified in
[`strategic-report.md`](./strategic-report.md) §5. Greenlit for execution.

### N1 — MCP Prompts (canonical workflows)

Expose pre-built workflows as first-class MCP `Prompts` (in addition to the
existing `Tools` and `Resources`). Lets agents discover the *right* tool chain
without re-deriving it.

- [ ] Add `@mcp.prompt()` decorators to `brand_mcp/server.py`:
  - [ ] `brand_check` — wraps `validate_brand_output` with usage example
  - [ ] `generate_brand_compliant_copy` — composer flow (context → prompt → validate)
  - [ ] `audit_built_site` — invokes the brand-compliance Skill
  - [ ] `propose_color` — fuzzy color lookup with disambiguation
- [ ] Verify `prompts/list` is advertised in the MCP capabilities handshake
- [ ] Update `.github/copilot-instructions.md` to mention the new prompts
- [ ] Smoke-test from Claude Desktop + VS Code Copilot

### N2 — Asset code-path index

Each asset record gets a `code_paths` array — every place in the repo that
references it. Foundation for Figma Code Connect later.

- [ ] `scripts/build-asset-index.mjs` — greps `site/`, `docs/`, `tailwind/` for
      asset references; writes `brand/asset-index.json`
- [ ] `package.json` script: `"index:assets": "node scripts/build-asset-index.mjs"`
- [ ] Extend `brand_mcp/composer/assets.py`:
  - [ ] Load `brand/asset-index.json` once at startup
  - [ ] Merge `code_paths: string[]` into each asset record
- [ ] CI: run `npm run index:assets` and fail if `brand/asset-index.json` is stale
- [ ] `site/src/pages/assets.astro` — show `code_paths` in the preview modal

### N3 — Telemetry-driven prioritization

JSONL telemetry behind an env flag, surfaced in an admin dashboard. Tells us
which tools/colors/components are actually used.

- [ ] `brand_mcp/utils/telemetry.py` — JSONL logger with daily rotation
- [ ] Env flag: `BRAND_MCP_TELEMETRY_ENABLED=1` (default off — privacy)
- [ ] Instrument all 10 tools at registration time
- [ ] `GET /api/stats` route — aggregates last 30 days
- [ ] `site/src/pages/admin/stats.astro` — canvas charts (top tools, top colors, error rate)
- [ ] Document the data model + retention in `brand_mcp/README.md`

### N4 — `AGENTS.md` at repo root

Adopt the cross-vendor `AGENTS.md` convention (Anthropic, OpenAI, OSS). Single
file at the root that any agent reads first.

- [ ] Create `/AGENTS.md` — identity, MCP tool table, no-go zones, validation flow, PR checklist
- [ ] Cross-link from `.github/copilot-instructions.md`
- [ ] Reference from root `README.md`

### N5 — Audit auto-fix mode

Extend the brand-compliance audit script with a preview/apply workflow for the
3 mechanical fixes (trademark, off-palette hex → nearest, headline case).

- [ ] `--fix` mode: writes `docs/brand-fixes-YYYY-MM-DD.patch` (no edits)
- [ ] `--apply` mode: writes the patch and applies it
- [ ] Auto-fix: `Solidigm®` → `Solidigm™`
- [ ] Suggest-fix: off-palette hex → nearest palette hex (commented in patch)
- [ ] Suggest-fix: ALL-CAPS headline → Title Case
- [ ] Update `.github/skills/brand-compliance/SKILL.md` with the new flags

---

## 🚧 Deferred / nice-to-have

- [ ] **Generate `ui-toolkit.min.css` from `build.js`** — currently `docs/ui-toolkit.min.css` is a manually-maintained file copied into `site/public/` at build time. Extend `build.js` to compile it from `tokens/` so the full toolkit CSS is source-driven and `docs/ui-toolkit.min.css` can be removed. This closes the last manually-edited CSS gap in the pipeline.
- [ ] Write-capable SharePoint tools (upload assets from agents)
- [ ] Redis-backed token store for production multi-instance deploys
- [ ] Figma MCP integration so the tokens → figma sync is bi-directional
- [ ] Published Docker image for the MCP server
- [ ] Azure Static Web Apps deployment with Entra SSO gate (if site moves off GH Pages)
- [ ] ESLint rule pack published as its own MCP prompt/resource

---

## 🔑 Required user actions

1. **Rotate the `M365_CLIENT_SECRET`** — the one in `Sharepoint-mcp-handoff.md` is now considered compromised. Generate a fresh secret in the `email-ai-test` app registration.
2. Decide on the MCP server's internal hostname (e.g. `brand-mcp.internal.solidigm.com`) and set `PUBLIC_MCP_URL` in both `site/.env` and the deployment environment.
3. Add the production redirect URI `{PROD_URL}/microsoft/callback` to the Entra app registration.
4. Grant admin consent for `Sites.Read.All` (delegated) and optionally the application permission of the same name for app-level access.
