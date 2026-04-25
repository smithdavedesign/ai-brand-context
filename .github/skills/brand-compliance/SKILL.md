---
name: brand-compliance
description: "Audit the Solidigm Astro site (or any built HTML directory) against the Solidigm brand quality gates. Use when verifying a site pre-release, running a full brand sweep, or producing a compliance report for stakeholders. Calls the solidigm-brand MCP server's /api/validate endpoint and emits a markdown report. Supports --fix (preview patch) and --apply (apply auto-fixes)."
argument-hint: "[site dir, default: site/dist] [--report path] [--fix] [--apply]"
---

# Brand Compliance Audit

Multi-step workflow that verifies every HTML page in a built site against the 16 Solidigm brand quality gates and produces a per-page markdown report.

## When to use

- Before releasing a new version of the Astro documentation site
- After a tokens update, to confirm downstream pages absorbed the change
- When a stakeholder asks "is the site on-brand?" — this gives them a receipt
- Audit any static HTML directory (not just this repo's `site/dist/`)

## Prerequisites

- `solidigm-brand` MCP server running on `http://localhost:8080` (or `BRAND_MCP_URL` env var points to it)
- Target site has been built — `.html` files exist (for this repo: `cd site && npm run build`)
- Node 18+ installed

## Procedure

1. **Ensure the MCP server is up:**
   ```bash
   curl -sf http://localhost:8080/api/health | jq
   ```
   If not running, start it: `cd brand_mcp && source .venv/bin/activate && python -m brand_mcp.server &`

2. **Build the Astro site** (if auditing this repo):
   ```bash
   cd site && npm run build && cd ..
   ```

3. **Run the audit script:**
   ```bash
   node .github/skills/brand-compliance/scripts/audit-pages.mjs site/dist
   ```
   The script walks every `.html` file under the target directory, extracts visible text + inline styles + CSS variable references, POSTs each to `/api/validate`, and aggregates the response.

4. **Review the emitted report** at `docs/brand-audit-<YYYY-MM-DD>.md`. Open it and scroll through:
   - Executive summary (overall grade, top issues, pages needing attention)
   - Per-page results table (errors, warnings, grade per page)
   - Detailed findings per page

5. **Report findings to the user.** Summarize:
   - Overall site grade (A+ through F) based on average per-page errors
   - Pages at or below a B grade that need remediation
   - The top 3 most common violations across the site
   - Suggested next actions (fix specific pages, update tokens, adjust a platform override)

## Grading scale

- **A+** — 0 errors, 0 warnings
- **A** — 0 errors, ≤ 2 warnings
- **B** — 1–2 errors
- **C** — 3–5 errors
- **F** — 6+ errors

## Scripts and resources

- [audit-pages.mjs](./scripts/audit-pages.mjs) — walks HTML, extracts text/styles, calls `/api/validate`, writes the report. Also supports `--fix` and `--apply` for the auto-fix pass over source files.

## Auto-fix mode (N5)

The audit script can also propose and apply mechanical fixes against the **source** tree (default `site/src/`).

```bash
# Preview only — write a patch and a markdown summary, no edits
node .github/skills/brand-compliance/scripts/audit-pages.mjs --fix

# Apply auto-fixes (the safe ones); suggestions stay in the patch for review
node .github/skills/brand-compliance/scripts/audit-pages.mjs --apply
```

Outputs:

- `docs/brand-fixes-YYYY-MM-DD.patch` — unified-diff-style patch with annotated severity
- `docs/brand-fixes-YYYY-MM-DD.md` — human-readable summary

Three rules:

1. **AUTO** — `Solidigm®` → `Solidigm™` (mechanical, applied with `--apply`)
2. **SUGGEST** — off-palette hex → nearest palette match within ΔE ≤ 60 (commented in patch only; never auto-applied)
3. **SUGGEST** — `<h*>ALL CAPS</h*>` → Title Case (commented in patch only)

Source-file scope can be overridden with `--fix-src <dir>`. The fix pass respects the same `<!-- brand-audit:exempt -->` blocks as the audit pass.

## Notes

- The audit is **report-only**. It does not fail CI. Upgrade to a CI gate (exit non-zero on errors) only after establishing a clean baseline.
- The audit checks built HTML, not source `.astro` files — Astro template syntax confounds the validator and built HTML is what users actually see.
- External assets (logos, SVGs, images) are excluded from text analysis. They are validated separately via the `list_assets` + `get_logo` MCP tools at source commit time.
- Reports are stored under `docs/brand-audit-*.md` and are gitignored by convention if you want them ephemeral — otherwise commit them as release evidence.

## Audit-exempt blocks

Some pages legitimately display off-brand content as **counter-examples** — the "what not to do" side of a before/after, a semantic-color swatch (`#ff0000` rendered to illustrate the error token), or a deliberately-broken demo. Wrap those sections in HTML comments to exclude them from validation:

```html
<!-- brand-audit:exempt -->
  <button style="background:#6600cc; border-radius:3px; font-family:Arial;">
    CLICK HERE  <!-- this is the "before" example -->
  </button>
<!-- /brand-audit:exempt -->
```

The wrapped content still renders in the browser; only the audit script strips it. Use sparingly — every exempt block is a trust line the next auditor has to read.
