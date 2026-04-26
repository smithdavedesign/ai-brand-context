# Tokens — Canonical Brand Tokens

This directory holds the **canonical, vendor-neutral Solidigm brand tokens**. Every Solidigm surface (web, print, iOS, partner content, internal tools, AI agents) consumes these.

> **Format:** [W3C Design Tokens Community Group spec (DTCG)](https://tr.designtokens.org/) — `$type` + `$value`.

---

## Layout

### Tier 1 — Primitives (pure brand language)

| File | Description | Status |
|------|-------------|--------|
| [`colors.json`](colors.json) | Full palette — 16 colors across Dark / Light / Accents groups | ✅ Existing |
| [`typography.json`](typography.json) | Sora type scale (web), Desktop + Mobile pairs | ✅ Existing |
| [`space.json`](space.json) | 4px-grid spacing scale (clean, no Bootstrap leftovers) | 🆕 New |
| [`breakpoints.json`](breakpoints.json) | Modern breakpoints (640/768/1024/1280/1440) + container widths | 🆕 New |
| [`radius.json`](radius.json) | Border-radius primitives (default 0 — sharp-corners brand rule) | 🆕 New |
| [`shape.json`](shape.json) | 45° notch language + clip-paths + border widths | 🆕 New |
| [`motion.json`](motion.json) | Durations, easings, transform primitives | 🆕 New |
| [`elevation.json`](elevation.json) | Shadow tokens (sparse — flat-design brand) | 🆕 New |
| [`icons.json`](icons.json) | UI icon atoms — double-arrow + accordion chevron: paths, sizes, themes, animations | 🆕 New |

### Tier 2 — Semantic Aliases (intent-driven)

| File | Description | Status |
|------|-------------|--------|
| [`semantic.json`](semantic.json) | Named aliases: `color.surface.primary`, `space.gap.md`, `typography.context.web`, etc. | 🆕 New |

### Compiled

| File | Description |
|------|-------------|
| [`index.json`](index.json) | Auto-merged file (legacy) — currently colors + typography only. Will be regenerated to include all primitives once `build.js` is updated. |

---

## Two color files — what's the difference?

`tokens/colors.json` (this directory) and `brand/colors.json` serve different purposes:

| | `tokens/colors.json` | `brand/colors.json` |
|-|----------------------|----------------------|
| **Format** | W3C DTCG (`$type`, `$value`) | Enriched object with WCAG notes, usage guidance, aliases |
| **Used by** | Build pipeline (`build.js`), Figma sync, dist outputs | MCP `get_color()` tool, brand compliance checks |
| **Authority** | Source of truth for CSS/SCSS/JS/TS dist files | Source of truth for AI-assisted brand guidance |
| **Edit when** | Adding/changing a color in the palette | Adding WCAG notes, usage examples, or color aliases |

Both files must stay in sync for any new color additions. The primitive hex values in `tokens/colors.json` are the ground truth.

---

## Conventions

- **Numeric space keys = pixels ÷ 4.** `space.4` = 16px, `space.10` = 40px, `space.25` = 100px.
- **Reference syntax:** `{color.Dark.Solidigm Purple}` resolves to the canonical hex.
- **Default rule for radius:** prefer `radius.none`. Sharp corners are the brand.
- **Default rule for elevation:** prefer `shadow.none`. Solidigm is a flat-design brand.
- **Default rule for motion:** `duration.base` + `easing.standard` unless the moment is brand-expressive.
- **Typography contexts coexist:** `typography.context.web` (Sora) for screens, `typography.context.print` (Sequel100) for print/brand collateral.
- **Icon fill rule:** double-arrow uses `currentColor` (theme-adaptive); accordion chevron + button arrow always use Electric Teal (`#00FFEC`) — hardcoded brand constant.

---

## Why three tiers?

```
primitive  →  semantic  →  platform
   ↓            ↓            ↓
"#4F00B5"   "color.surface.primary"   web/ios/print overrides
```

- **Primitives** rarely change. They're the building blocks.
- **Semantics** describe intent. They survive redesigns.
- **Platform overrides** live elsewhere (`brand/platforms/*.md`) when web vs. print vs. iOS need different defaults.

AI agents should prefer **semantic names** when generating guidance (`color.surface.primary`, `space.gap.md`) — they communicate intent, not implementation.

---

## Provenance

The new primitives (`space`, `breakpoints`, `radius`, `shape`, `motion`, `elevation`, `semantic`) were derived from a comparative audit of two Solidigm web codebases (Storybook + AEM `docs/v3/`). See:

- [`docs/storybook-scss-audit.md`](../docs/storybook-scss-audit.md)
- [`docs/aem-vs-storybook-audit.md`](../docs/aem-vs-storybook-audit.md)

Those repos are evidence. The canonical values live here.
