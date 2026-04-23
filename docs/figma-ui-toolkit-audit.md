# Figma UI Toolkit Audit — Solidigm Design System 3.0

**Generated:** 2025-06-18
**Figma file:** [Solidigm Design System 3.0 (New Version)](https://www.figma.com/design/Ei8AT6lR0173XP1v8kY3JJ)
**Scope:** All 10 sections of the UI Tool Kit page
**Purpose:** Identify all tokenizable values beyond the existing typography & color tokens

---

## Section Map

| # | Section | Node ID | Tokenizable? | Status |
|---|---------|---------|-------------|--------|
| 01 | DT + MB Grid | 791:2038 | **YES** — spacing/layout | New tokens needed |
| 02 | Type Styles | 791:1493 | **YES** — already in package | Drift documented in figma-token-diff.md |
| 03 | Color Palette | 791:1998 | **YES** — already in package | ✅ Exact match confirmed |
| 04 | Background | 791:2473 | **YES** — semantic backgrounds | New tokens needed |
| 05 | Buttons + Links | 791:2164 | **YES** — component tokens | Internal Figma inconsistency found |
| 06 | Form Fields | 791:2261 | **YES** — state colors | New tokens needed |
| 07 | Image Containers | 791:2269 | No — visual guidelines only | No action |
| 08 | Iconography | 791:2312 | **Partial** — icon color/sizes | Minor token candidates |
| 09 | Interactivity | 791:2362 | **YES** — states, new colors | New tokens needed |
| 10 | Photography | 791:2438 | No — art direction only | No action |

---

## 01. DT + MB Grid — Spacing Tokens

### Desktop Grid
| Property | Value |
|----------|-------|
| Viewport width | 1920px |
| Columns | 12 |
| Margin | 80px |
| Gutter | 20px |
| Component padding | 150px |
| Text padding | 40px |

### Mobile Grid
| Property | Value |
|----------|-------|
| Viewport width | 393px |
| Columns | 5 |
| Margin | 20px |
| Gutter | 20px |
| Component padding | 70px |
| Text padding | 30px |

### Proposed Token Names
```
spacing.grid.dt.viewport: 1920
spacing.grid.dt.columns: 12
spacing.grid.dt.margin: 80
spacing.grid.dt.gutter: 20
spacing.grid.dt.padding.component: 150
spacing.grid.dt.padding.text: 40
spacing.grid.mb.viewport: 393
spacing.grid.mb.columns: 5
spacing.grid.mb.margin: 20
spacing.grid.mb.gutter: 20
spacing.grid.mb.padding.component: 70
spacing.grid.mb.padding.text: 30
```

---

## 04. Background — Semantic Page Colors

Three page-level background categories define color usage as a wayfinding system:

### Inspirational Pages
- **Primary**: Solid Black (#000000) + Black-to-Dark-Gray gradient (#000000 → #52514F)
- **Use for**: Pages with brand focus, exploration (Homepage, Who We Are)

### Informative Pages
- **Primary**: White (#FFFFFF)
- **Use for**: Info-heavy, conversion flow, support, checkout (Cart, Support Center)

### Branded Moments
- **Primary**: Solidigm Purple (#4F00B5) or Ultra Dark Purple (#160231)
- **Use for**: Key brand emphasis sections

### Proposed Token Names
```
background.page.inspirational: #000000
background.page.inspirational.gradient.from: #000000
background.page.inspirational.gradient.to: #52514F
background.page.informative: #FFFFFF
background.page.branded.primary: #4F00B5
background.page.branded.dark: #160231
```

### Color Legend (from section header)
Small swatches shown at top of section confirm the full palette used across backgrounds:

| Row | Colors |
|-----|--------|
| Dark row | #21201F, #000000, #00083F, #2F006B, #160231 |
| Light row | #FFFFFF (outlined), #F5F3F1 |

All these colors already exist in `color.styles.tokens.json` — this section maps **semantic meaning** to existing colors.

---

## 05. Buttons + Links — Internal Figma Inconsistency

**ISSUE**: The Buttons section uses typography values that differ from the Type Styles section:

| Token | Type Styles Section | Buttons Section | Discrepancy |
|-------|-------------------|-----------------|-------------|
| DT Body | 16px / 300 / 22px | 18px / 200 / 22px | fontSize + weight differ |
| DT Caption | 16px / 300 / 22px / ls:0 | 16px / 300 / 22px / ls:1 | letterSpacing added |

This indicates typography was updated unevenly within Figma itself. The Type Styles section should be treated as canonical.

---

## 06. Form Fields — Component State Tokens

Figma component variants define form field states:

### Variant Properties
- **State**: Default, Hover, Input, Dropdown, Error
- **Background**: Dark Gray, White, Error

### Token Candidates
```
form.field.state.default.border: (needs design context fetch)
form.field.state.hover.border: (needs design context fetch)
form.field.state.error.border: (needs design context fetch)
form.field.background.dark: (needs design context fetch)
form.field.background.light: (needs design context fetch)
```

> **Note**: Full design context not yet fetched for this section. Exact color values TBD.

---

## 08. Iconography — Icon System

### Icon Catalog
- **40+ content icons** in a grid layout (Hardware, Connect, Explore, Cyber, Performance, Storage, etc.)
- All rendered in **Solidigm Purple (#4F00B5)** on white background
- Sourced from Brand Guidelines

### Wayfinding Icons
| Icon | Function |
|------|----------|
| Arrow (double chevron) | Guide users to destinations (interactive hover) |
| Accordion – Open | Indicates content being revealed |
| Accordion – Close | Indicates content being collapsed |

### Footer / Social Icons
- X/Twitter (~19px), YouTube (24×16px), LinkedIn (18px), Facebook (9×18px)
- All rendered in dark (#21201F or black)

### Unique Components
- **DT Play Button**: Circle with play triangle (Solidigm Purple)
- **MB Play Button**: Mobile-sized variant
- **Pause Button**: Two vertical bars (#4F00B5)

### Token Candidates
```
icon.color.default: #4F00B5
icon.color.social: #21201F
```

---

## 09. Interactivity — Richest Section for New Tokens

### Product Card States

| State | Background | Text | Border | Corner | CTAs |
|-------|-----------|------|--------|--------|------|
| Default | White | Black | #4F00B5 (1px) | Square | Hidden |
| Hover | #4F00B5 | White | — | 45° cut | Visible |

### CTA Buttons (on hover card)

| Button | Background | Text | Border |
|--------|-----------|------|--------|
| View Details | White | #13032F (Ultra Dark Purple) | — |
| Compare | #4F00B5 | White | White (1px) |

### NEW COLOR DISCOVERED: #13032F
- **Ultra Dark Purple** — used for primary CTA text on white buttons
- This is NOT in the current `color.styles.tokens.json`
- Close to but distinct from #160231 (Dark Purple, already in tokens)

### Sticky In-Page Nav

| Element | Value |
|---------|-------|
| Bar background | #21201F (Dark Gray) |
| Active tab underline | #00FFEC (Electric Teal) |
| Active tab text | White, opacity 100% |
| Inactive tab text | White, opacity 50% |
| Tab typography | Sora SemiBold 9.62px / ls:2 / uppercase |
| Bar border | Electric Teal line at bottom |

### Pagination

| Platform | Behavior |
|----------|----------|
| Desktop | Auto-play, pause on hover or click, timer progress bar |
| Mobile | No autoplay, manual swipe/tap, full-width timer bars |

### Interactive Color Semantic Map
From the section's color blocks:
```
interactive.default: #4F00B5      (Solidigm Purple — clickable elements)
interactive.hover: #2F006B        (Dark Purple — hover/selected state)
interactive.active: #00FFEC       (Electric Teal — active indicator)
interactive.cta.primary.bg: white
interactive.cta.primary.text: #13032F
interactive.cta.secondary.bg: #4F00B5
interactive.cta.secondary.text: white
interactive.card.default.bg: white
interactive.card.default.border: #4F00B5
interactive.card.hover.bg: #4F00B5
interactive.card.hover.text: white
interactive.nav.bg: #21201F
interactive.nav.active: #00FFEC
interactive.nav.text.active: rgba(255,255,255,1)
interactive.nav.text.inactive: rgba(255,255,255,0.5)
```

### Typography Used in Section
| Token | Values | Match to Source JSON? |
|-------|--------|--------------------|
| DT Accordion | 32/300/38 | ✅ Matches Figma 3.0 (source has 200 weight) |
| DT Body 1 | 18/200/22 | ⚠️ Uses older 200 weight (Figma Type Styles says 300) |
| DT Button Link | 14/600/18/ls:2 | ✅ Match |
| DT Disclaimer | 12/200/14 | ⚠️ Uses older 200 weight (Figma Type Styles says 300) |
| DT Category | 14/600/18/ls:2 | ✅ Match |
| DT Breadcrumb | 10/700/16/ls:2 | ✅ Match |

This confirms the same inconsistency found in 05. Buttons — the Interactivity section was built before the weight bump from 200→300 was applied in Type Styles.

---

## 07. Image Containers — Visual Guidelines Only

- **90° and 45° angle** cropping rules for brand image containers
- Do's: Use structured crops, keep brand marks abstract, tight controlled cropping, align to grid
- Don'ts: Don't stack containers, no irregular angles, no freeform cropping, no stretch/skew/distort
- Used in: Website layouts, UI design elements
- **No tokenizable values** — implementation guidance only

---

## 10. Photography — Art Direction Only

Three photography categories:
1. **Background**: Abstract/atmospheric backdrops (terrain, waveforms)
2. **Mockups**: Clean product shots with realistic lighting, Solidigm branding
3. **Inspirational/Human Elements**: Intelligent, composed portraits; hands-on detail shots

- **No tokenizable values** — art direction and style guidance only

---

## Summary: New Token Candidates

### High Priority (structured, numeric, directly usable)

| Category | Count | Source Section |
|----------|-------|---------------|
| Grid/Spacing | 12 tokens | 01. Grid |
| Semantic Backgrounds | 6 tokens | 04. Background |
| Interactive States | 14 tokens | 09. Interactivity |

### Medium Priority (needs design context or brand team input)

| Category | Count | Source Section |
|----------|-------|---------------|
| Form Field States | ~5 tokens | 06. Form Fields |
| Icon Colors | 2 tokens | 08. Iconography |

### New Color: #13032F (Ultra Dark Purple)
- Found in 09. Interactivity as CTA button text
- Not in current token package
- Must be added to `color.styles.tokens.json`

### Internal Figma Drift Confirmed
Sections 05, 09 use **fontWeight 200** for DT Body, DT Disclaimer, DT Accordion — while section 02 (Type Styles) shows **fontWeight 300**. This confirms the 200→300 weight migration was applied to the Type Styles master but not propagated to component instances across the toolkit.

---

## Decision Checklist (extends figma-token-diff.md)

- [ ] **Grid tokens** — Add to v1.1.0?
- [ ] **Semantic background tokens** — Add to v1.1.0?
- [ ] **Interactive state tokens** — Add to v1.1.0?
- [ ] **#13032F (Ultra Dark Purple)** — Add to color palette?
- [ ] **Form field tokens** — Fetch exact values and add?
- [ ] **Icon color tokens** — Add or defer?
- [ ] **Figma weight drift (200→300)** — Flag to design team for component sync?

---

*This audit covers all 10 sections of the Figma UI Tool Kit page. Combine with figma-token-diff.md for a complete brand token status.*
