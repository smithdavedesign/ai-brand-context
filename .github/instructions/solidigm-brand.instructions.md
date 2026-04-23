---
description: "Use when authoring or modifying Solidigm brand-facing UI, copy, markup, or design tokens — covers color palette, typography, trademark, voice, and hard do-nots. Enforces the same rules as the validate_brand_output MCP tool."
applyTo: "**/*.{astro,tsx,jsx,ts,js,css,scss,md,mdx,html,vue}"
---

# Solidigm Brand Rules (Enforced)

These rules mirror `brand/quality-gates.yaml`. Violations should be fixed, not shipped. When in doubt, call the `solidigm-brand` MCP tools — `get_color`, `get_brand_guidelines`, `validate_brand_output`.

## Color — the 17-hex palette

- **Allowed hex values only.** Primary: `#4f00b5` (Solidigm Purple), `#ffffff`, `#21201f`, `#160231`. Purple family: `#8d59cf`, `#b9a4da`, `#f0e6fb`. Gray family: `#f5f3f1`, `#e9e8e7`, `#a6a6a6`, `#52514f`. Accents (≤10% of any composition): `#00ffec` (Electric Teal), `#ff6c5a` (Warm Coral), `#ffd000` (Signal Yellow). Chart-only: `#007fff`, `#00a651`, `#ed1c24`.
- Any hex outside this set → replace with the nearest approved token.
- Accent colors are for **emphasis only**. Do not use as backgrounds, borders, or dominant elements.
- Reference via tokens, not raw hex: `var(--solidigm-color-solidigm-purple)` or `colors.solidigmPurple`.

## Typography — three typefaces only

- **Sora** — display / headlines
- **Noto Sans** — body / UI / multilingual
- **Avenir Next LT Pro** — legacy print fallback only
- No other `font-family` values. No Arial, Helvetica, Roboto, Inter, Comic Sans, system-ui fallback alone — always name the approved face first.

## Trademark

- Use **™** (`&trade;`) after `Solidigm` on first mention per page/doc.
- **Never** use `®` — Solidigm is not a registered trademark.
- Product names: `Solidigm™ DC PS1010`, not `Solidigm DC PS1010` on first mention.

## Headings

- **Never all-uppercase.** Use sentence case or title case.
- CSS `text-transform: uppercase` on headings is a violation.

## Voice

- Confident, not arrogant. Technical, not dense. Human, not casual.
- Avoid: "Welcome to the future of…", "revolutionary", "game-changing", "disruptor".
- Prefer: concrete numbers, measurable outcomes, customer-verb constructions ("Customers run more queries per rack").

## Logo

- Clear space = the height of the `S` mark on all sides.
- Never alter the logo (no gradients, shadows, recolors outside the 4 approved colors, stretches, rotations, outlines).
- Approved colors: black (`#21201f`), purple (`#4f00b5`), blue (`#160231`), white (`#ffffff`).

## Generative AI content

- Disclose AI-generated imagery where used externally.
- Never depict real Solidigm employees, customers, or partners with AI.
- Never generate AI copy that makes product performance claims without being fact-checked against a Solidigm datasheet.

## How to verify

Before committing brand-facing changes, run one of:

- `validate_brand_output` MCP tool on the content, or
- `/brand-check` prompt against the file, or
- `brand-compliance` Skill for a full site sweep.
