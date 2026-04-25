# Documentation Index

Map of every document in `docs/`. Start here.

## Live docs (canonical)

| Doc | Purpose |
|-----|---------|
| [`architecture.md`](./architecture.md) | System architecture: mermaid diagrams + sequence flows |
| [`roadmap.md`](./roadmap.md) | Phased delivery plan with status per item |
| [`strategic-report.md`](./strategic-report.md) | Agentic-AI strategy — Now/Next/Later, anti-patterns, KPIs |
| [`design-system-integration.md`](./design-system-integration.md) | How this repo maps to the Solidigm Storybook + Figma 3.0 component library |
| [`one-stop-shop-brand-system.md`](./one-stop-shop-brand-system.md) | Full essay: why a modern brand belongs in one repo |
| [`one-stop-shop-brand-system.exec.md`](./one-stop-shop-brand-system.exec.md) | One-page TL;DR of the essay |
| [`ui-toolkit.min.css`](./ui-toolkit.min.css) | Compiled UI toolkit CSS — synced into `site/public/` at build time |

## Audit reports (release evidence)

The `brand-compliance` Skill writes one report per audit run.

- `brand-audit-YYYY-MM-DD.md` — output of `node .github/skills/brand-compliance/scripts/audit-pages.mjs`

## Archived (historical, not live)

The [`_archive/`](./_archive/) subfolder contains pre-build planning docs and
legacy references that were superseded by the live system. They are kept for
historical context (and to make blame/log traceable), **not** as guidance.

| Archived doc | Why archived |
|--------------|--------------|
| `_archive/Brand-AI-Context-PRD.md` | Pre-build draft v2 — superseded by [`architecture.md`](./architecture.md) + [`strategic-report.md`](./strategic-report.md) |
| `_archive/brand-context-ai-PRD.md` | Pre-build draft v1 — same |
| `_archive/brand-guidelines.md` | Original 120-page narrative — split into `brand/*.md` topic files |
| `_archive/figma-token-diff.md` | Snapshot diff (Apr 2025) — folded into [`design-system-integration.md`](./design-system-integration.md) |
| `_archive/figma-ui-toolkit-audit.md` | Audit snapshot (Jun 2025) — folded into same |
| `_archive/solidigm_brand_architecture.html` | Older diagram — superseded by mermaid in [`architecture.md`](./architecture.md) |
| `_archive/text.styles.tokens.json` | Figma type-style export — superseded by [`tokens/typography.json`](../tokens/typography.json) |

> **Rule of thumb:** if the brand changes, do _not_ edit anything in
> `_archive/`. Edit `tokens/`, `brand/`, or `docs/{architecture,roadmap,strategic-report,design-system-integration}.md`.

## New here?

1. Read [`architecture.md`](./architecture.md) for the system shape
2. Read [`strategic-report.md`](./strategic-report.md) for the strategy
3. Skim [`roadmap.md`](./roadmap.md) for current status
4. See [`../README.md`](../README.md) for everything you can do with the MCP
