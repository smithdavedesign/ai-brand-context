# Design system integration

How the `ai-brand-context` repo connects to the broader Solidigm design ecosystem
— the corporate **Storybook**, **Figma 3.0** files, and the local **Figma MCP**
server.

This is a living doc. When a Figma file moves or a Storybook URL changes, edit
this doc (not `_archive/figma-token-diff.md`).

---

## 1. The four design surfaces

```
                    ┌─────────────────────────────────────────┐
                    │       SOLIDIGM DESIGN ECOSYSTEM         │
                    └─────────────────────────────────────────┘

  Figma 3.0                Storybook                ai-brand-context (this repo)
  (design source)          (component runtime)      (brand source of truth + MCP)

  • Dotcom 3.0 file        • Live, themed UI        • Tokens (W3C DTCG)
  • Design System 3.0      • Used by solidigm.com   • Brand guidelines
    component library      • Protected URL          • UI toolkit CSS
  • Figma variables        • Stack: corporate       • MCP server (15 tools)
    drive published                                 • Astro docs site
    tokens

                          Local Figma MCP server
                          (separate process — read-only Figma access for AI)
```

Each surface has a different audience and a different update cadence. This
repo is the **bridge**: it harmonizes design decisions made in Figma with code
patterns used in Storybook, and exposes them to AI agents through MCP.

---

## 2. Figma files

Two canonical Figma files. Both live in the Solidigm corporate Figma org.

| File | Figma file key | Owner | What lives there |
|------|----------------|-------|------------------|
| **Dotcom 3.0** | `BioUSVD6t51ZNeG0g9AcNz` | solidigm.com team | Page templates, hero patterns, marketing layouts |
| **Design System 3.0** | `Ei8AT6lR0173XP1v8kY3JJ` | Brand / DS team | Component library, variables, type styles, color styles |

> The file keys are stable. Use them to construct `https://www.figma.com/file/<KEY>` URLs.

### Deep links currently referenced

When debugging or syncing, these specific frames are the "ground truth":

- Design System 3.0 — Color page: `?node-id=...` (record the node-id when first opened so future syncs can re-anchor)
- Design System 3.0 — Type ramp: `?node-id=...`
- Dotcom 3.0 — Component usage examples: `?node-id=...`

> **Convention:** when you take a token-diff snapshot, drop it as
> `docs/figma-snapshot-YYYY-MM-DD.md` (not as a generic name) so the date is
> visible in `git log`.

---

## 3. Storybook (corporate)

URL: `https://solidigmstorybook.z5.web.core.windows.net/`

- **Status:** protected — corporate auth required
- **Do not scrape.** Stories are not part of this repo's CI loop
- **What it provides:** runtime previews of Storybook components consumed by
  solidigm.com. Useful as a visual reference when implementing new patterns
  in `site/`
- **What this repo provides back:** the canonical color, type, spacing, and
  copy rules that those Storybook components must respect

If a component in Storybook drifts from a token in this repo, this repo wins
(tokens are the source of truth). Open a PR against the Storybook repo to
re-align.

---

## 4. Local Figma MCP server (separate process)

A separate Figma MCP server runs locally and gives AI agents read-only access
to Figma files (variables, components, frames). It is **not** part of this
repo's build, but it composes well with `solidigm-brand`:

```
┌──────────────────┐     figma_get_variables      ┌────────────────┐
│   AI agent       │ ───────────────────────────► │  figma MCP     │
│  (Claude/GPT)    │                              │  (read-only)   │
│                  │ ◄─── color hex from Figma ── └────────────────┘
│                  │
│                  │     get_color, validate_brand_output
│                  │ ───────────────────────────► ┌────────────────┐
│                  │                              │ solidigm-brand │
│                  │ ◄─── canonical token + ───── │  MCP (this)    │
│                  │      pass/fail               └────────────────┘
└──────────────────┘
```

Pattern: ask the **figma MCP** for what a designer specced; ask
**solidigm-brand** for the canonical token; reconcile. If they disagree, the
canonical token wins and the Figma file is updated to match.

---

## 5. Token sync workflow

1. Designer changes a variable in **Design System 3.0**
2. Brand owner exports affected variables (Figma → Tokens plugin) into
   `figma/incoming/YYYY-MM-DD.json` (gitignored)
3. Run `npm run diff:figma -- figma/incoming/YYYY-MM-DD.json` — emits a
   dated drift report at `docs/figma-snapshot-YYYY-MM-DD.md`
4. Reconcile: update `tokens/colors.json` / `tokens/typography.json` for
   anything the canonical should adopt; update Figma for anything the
   canonical should retain
5. `npm run build` → regenerates `dist/tokens.css`, `dist/tokens.js`,
   `figma/tokens.json`
6. PR + CI → the `mcp-smoke-test` job re-loads tokens, validates 10 tool
   contracts; the `asset-index-freshness` job verifies `brand/asset-index.json`
   is current
7. Storybook team pulls the published `@solidigm/brand-tokens` package on
   their next release

This repo is **upstream** of Storybook and **downstream** of Figma.

---

## 6. UI toolkit ↔ Figma component mapping

The Solidigm UI toolkit (compiled to `docs/ui-toolkit.min.css`) defines `tk-*`
classes that map roughly 1:1 to Figma 3.0 components. The mapping is
discovered at runtime via the `get_ui_toolkit_class` MCP tool — no static
table is required.

When new Figma components ship:

1. Add the corresponding selector to `docs/ui-toolkit.min.css`
2. Document it in `brand/ui-toolkit.md` (description + usage notes)
3. Restart the MCP server (cache reloads on startup)
4. Verify with `mcp call get_ui_toolkit_class --name tk-newcomponent`

---

## 7. Future: Figma Code Connect

Figma's **Code Connect** lets a Figma component point at a code path. Once we
have an asset code-path index (see Phase 9 / N2 in the roadmap), we can write
Code Connect manifests that resolve Figma components → Storybook stories →
`tk-*` classes. This is tracked in [`strategic-report.md`](./strategic-report.md)
under the Next plays.
