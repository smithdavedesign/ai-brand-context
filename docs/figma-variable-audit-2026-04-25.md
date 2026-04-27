# Figma Variable Audit — 2025-04-25

> Produced via live Figma MCP (`localhost:3845`) against the Solidigm Design
> System 3.0 library and the Dotcom 3.0 UI Toolkit page.

---

## 1. Data sources

| Source | File key | Node / Library |
|--------|----------|----------------|
| **Solidigm Design System 3.0 (New Version)** | `Ei8AT6lR0173XP1v8kY3JJ` | Library `lk-5c495…` |
| **Solidigm Dotcom 3.0 — Dayani** | `BioUSVD6t51ZNeG0g9AcNz` | Page `15967:1674` ("🖌️ V2 UI Tool Kit") |
| **Canonical tokens** | — | `tokens/colors.json`, `tokens/typography.json` |

---

## 2. Figma variables inventory

### 2.1 Color variables (Collection: "Primitives")

Found via `search_design_system` in the DS 3.0 library:

| Variable name | Type | Collection |
|---------------|------|------------|
| Solidigm Purple | COLOR | Primitives |
| Purple | COLOR | Primitives |
| Light Purple | COLOR | Primitives |
| Dark Purple | COLOR | Primitives |
| Ultra Dark Purple | COLOR | Primitives |
| Electric Teal | COLOR | Primitives |

**6 color variables** published in the library.

### 2.2 Fill styles

| Style name | Type | Library |
|------------|------|---------|
| Dark / Solidigm Purple | FILL | DS 3.0 (New Version) |
| Dark / Purple | FILL | DS 3.0 (New Version) |
| Dark / Dark Purple | FILL | DS 3.0 (New Version) |
| Dark / Ultra Dark Purple | FILL | DS 3.0 (New Version) |
| Dark / Light Purple | FILL | DS 3.0 (New Version) |
| Accents / Electric Teal | FILL | DS 3.0 (New Version) |

Also duplicated in the Dotcom 3.0 file as local styles.

### 2.3 Text styles

| Style name | Type | Library |
|------------|------|---------|
| Desktop / DT Button Link | TEXT | DS 3.0 (New Version) |
| Mobile / MB Button Link | TEXT | TEXT | DS 3.0 (New Version) |

Only 2 text styles published as library styles. The remaining 26 type styles
(Hero, H1–H6, Body, Caption, etc.) exist in the UI Toolkit comp page as
visual specifications but are **not published as Figma text styles**.

### 2.4 Non-color variables

Exhaustive searches for spacing, radius, shadow, border, padding, margin, gap,
breakpoint, and elevation returned **zero results** across all Figma libraries.

**No spacing, radius, shadow, or elevation variables exist in Figma.**

---

## 3. Color comparison — Figma vs canonical tokens

### Method

1. Pulled screenshots of the Color Palette section (`15967:1951`) via
   `get_screenshot`.
2. Read annotation text from the metadata XML for cross-reference.
3. Compared against `tokens/colors.json`.

### Results

| Token name | Canonical hex | Figma annotation | Swatch pixel | Status |
|------------|---------------|------------------|--------------|--------|
| Solidigm Purple | `#4f00b5` | `#4F00B5` (in button specs) | `#4809AE` | ✅ Annotation matches |
| Light Purple | `#8d59cf` | — | `#8658C8` | ⚠️ Pixel drift |
| Dark Purple | `#2f006b` | — | `#2F046A` | ≈ Close |
| Ultra Dark Purple | `#160231` | — | `#13032F` | ⚠️ Pixel drift |
| Dark Blue | `#00083f` | — | `#02083C` | ≈ Close |
| Dark Grey | `#21201f` | — | `#21201E` | ≈ Close |
| Black | `#000000` | — | — | ✅ |
| White | `#ffffff` | — | `#FFFFFF` | ✅ |
| Light Gray | `#f5f3f1` | — | `#F4F3F1` | ≈ Close |
| Gray | `#a5a29d` | — | `#A5A39F` | ≈ Close |
| Medium Gray | `#52514f` | — | `#52514F` | ✅ |
| Electric Teal | `#00ffec` | `#00FFEC` (in button specs) | `#75FBEC` | ✅ Annotation matches |
| Electric Pink | `#ea11bc` | — | `#D733B7` | ⚠️ Pixel drift |
| Orange | `#ffa42c` | — | `#F2A94A` | ⚠️ Pixel drift |

### Interpretation

The **annotation text** in Figma button specifications references canonical
values (`#4F00B5`, `#00FFEC`), confirming the design library intends to use our
token values. The pixel-level differences in the screenshot swatches are
artifacts of:

- Figma's PNG export color profile conversion
- Possible opacity or blend modes on swatch component instances
- Screenshot compression

**Conclusion:** The 6 published Figma color variables likely store the correct
canonical hex values. The swatches in the toolkit page are visual comps, not
authoritative color definitions.

---

## 4. Typography comparison

### Canonical tokens (28 styles)

| Group | Styles | Font | Weight |
|-------|--------|------|--------|
| Desktop | Hero, H1–H6, Accordion, Body, Caption, Category, Button, Disclaimer, Breadcrumb | Sora | 200 (light) or 600/700 (small text) |
| Mobile | MB Hero, MB H1–H6, MB Accordion, MB Body, MB Caption, MB Category, MB Button, MB Disclaimer, MB Breadcrumb | Sora | Same as desktop |

### Figma coverage

| Token | In Figma text styles? | In toolkit comp? |
|-------|-----------------------|------------------|
| DT Button / MB Button | ✅ Published style | ✅ |
| DT Hero – DT Breadcrumb | ❌ Not published | ✅ Visual spec only |
| MB Hero – MB Breadcrumb | ❌ Not published | ✅ Visual spec only |

**Gap:** 26 of 28 type styles are *specified* in the toolkit page but **not
published as Figma text styles**. Only DT Button Link and MB Button Link are
library-level styles. Designers must manually apply font properties rather than
selecting from a style menu.

### Font family note

Canonical tokens use **Sora** throughout. The brand instructions also list
**Noto Sans** (body/UI) and **Avenir Next LT Pro** (legacy print).
Older documentation (`AGENTS.md`) references Sequel100 and Roboto — these are
from a previous brand generation and should be updated once the Sora migration
is complete across all docs.

---

## 5. UI Toolkit page — section inventory

Page: `15967:1674` in Dotcom 3.0 (Dayani), dated 11/17/25.

| # | Section | Node ID | Tokenizable content |
|---|---------|---------|---------------------|
| — | TOC | `15967:1914` | — |
| 01 | DT + MB Grid | `15967:1991` | Breakpoints, column counts, gutter widths |
| 02 | Type Styles | `15967:1677` | Font sizes, weights, line heights (28 styles) |
| 03 | Color Palette | `15967:1951` | 13 colors + groupings |
| 04 | Background | `15967:2589` | Color application rules per page type |
| 05 | Buttons + Links | `15967:2117` | Border radius, padding, hover colors |
| 06 | Form Fields | `15967:2316` | Input heights, border, focus ring, error states |
| 07 | Photo Styling | `15967:2385` | Crop ratios, overlay specs |
| 08 | Iconography | `15967:2428` | Icon sizing, social icon set |
| 09 | Interactivity | `15967:2478` | Card hover, nav, carousel, 45° blades |
| 10 | Photography | `15967:2554` | Photography art direction guidelines |

---

## 6. Gap summary

| Category | In tokens/ | In Figma vars | In toolkit comp | Gap |
|----------|-----------|---------------|-----------------|-----|
| Colors (14) | ✅ 14 | 6 vars + 6 fill styles | ✅ 13 swatches | Minor — 8 colors not as variables |
| Typography (28) | ✅ 28 | 2 text styles | ✅ 28 visual specs | **Major** — 26 styles not published |
| Spacing | ❌ | ❌ | ✅ Grid specs | **Major** — no tokens anywhere |
| Border radius | ❌ | ❌ | ✅ Button/card specs | **Major** — no tokens |
| Shadows / elevation | ❌ | ❌ | ❌ | Not specified |
| Breakpoints | ❌ | ❌ | ✅ Grid section | **Medium** — only in comp |
| Form field states | ❌ | ❌ | ✅ Full spec | Component-level |
| Iconography | ❌ | ❌ | ✅ Inventory | Asset-level |

---

## 7. Recommendations

1. **Publish all 28 text styles** in the DS 3.0 Figma library so they're
   selectable by designers (vs. manual font property entry).
2. **Add missing 8 colors as variables** in Primitives (Light grays, Dark Blue,
   Black, Electric Pink, Orange).
3. **Extract spacing tokens** from the DT + MB Grid section and Buttons + Links
   padding specs — these are the highest-value net-new tokens.
4. **Extract border-radius tokens** from Buttons + Links and Card components.
5. **Create breakpoint tokens** from the Grid section (likely 375px, 768px,
   1024px, 1440px based on standard Figma frames).
6. **Shadows/elevation** — not currently specified in Figma; defer until the
   design team adds elevation guidance.
7. **Align AGENTS.md font references** — update Sequel100/Roboto mentions to
   Sora/Noto Sans to match current brand generation.
