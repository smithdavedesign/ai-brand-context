# AEM Corporate vs Storybook — Evidence for Canonical Tokens

> **Date:** 2026-04-25
> **Sources (read-only reference):**
> - Storybook: `enterprise_apps.marketing.application.solidigm_com_storybook` (65 SCSS files)
> - AEM Corporate: `docs/v3/styles/` (79 SCSS files, copied here as reference snapshot)
> **Purpose:** Compare the two web implementations to inform canonical brand-token design in this repo.
> **Status:** Both source repos are read-only inputs. This project ships no changes to either.

---

## 1. Headline Finding

**The two repos share the SAME design foundation.** Every primitive (color, spacing, typography, breakpoints, mixins, themes) is byte-identical or trivially equivalent. They are the same design system implemented in two delivery vehicles:

| Repo | Role |
|------|------|
| **Storybook** | Component reference / design QA / handoff to authors |
| **AEM (`docs/v3/`)** | Production code that ships on solidigm.com |

The AEM repo is essentially Storybook + 14 site-specific molecules + 2 site-specific atoms + minor evolutionary fixes.

---

## 2. Foundation Parity Matrix

| Token Category | Storybook | AEM `v3/` | Match? |
|---------------|-----------|-----------|--------|
| `$spacer` (1rem base) | ✅ | ✅ | **Identical** |
| `$spacers` map (0–16) | ✅ | ✅ | **Identical** |
| `$grid-breakpoints` (xs–xxl) | ✅ | ✅ | **Identical** |
| `$gap-mobile/desktop/20` | ✅ | ✅ | **Identical** |
| `$padding-mobile/tablet/desktop` | ✅ | ✅ | **Identical** |
| `$inlinePaddings` (lg/xl/xxl) | ✅ | ✅ | **Identical** |
| `$column-space` map | ✅ | ✅ | **Identical** |
| `$iconSize` map | ✅ | ✅ | **Identical** |
| `$clipPaths` map (notch corners) | ✅ | ✅ | **Identical** |
| 18 color SCSS vars | ✅ | ✅ | **Identical hex** |
| `$colors` map | ✅ | ✅ | **Identical** |
| Sora font + 6 weights | ✅ | ✅ | **Identical** |
| Font size pairs (14) | ✅ | ✅ | **Identical** |
| Line height pairs (14) | ✅ | ✅ | **Identical** |
| `fluid-clamp()` function | ✅ | ✅ | **Identical** |
| `vwMobile()` / `vwDesktop()` | ✅ | ✅ | **Identical** |
| `responsive-inline-padding` mixin | ✅ | ✅ | **Identical** |
| Border-radius philosophy (0) | ✅ | ✅ | **Identical** |
| Themes (light/dark/purple/etc.) | 6 | **7** (adds `gray-mid`) | AEM extended |

**Conclusion:** The shared foundation IS the design system. There is no foundation drift between the two repos.

---

## 3. Differences

### 3.1 AEM Has That Storybook Doesn't

**Base layer additions:**
- `_table.scss` — table element styles (presumably for RTE-authored content)
- `_typography-vars.scss` — variable-only version of typography (no CSS rules emitted; for use in component-scoped bundles like the chatbot widget, where global selectors would leak)

**Atoms (2):**
- `_contentSearch.scss` — promoted from molecule to atom
- `_pagination.scss` — pagination control

**Molecules (14 net new — site infrastructure not in storybook):**
- `_careersListings.scss` — careers page
- `_chatbot.scss` + `_chatbot-rich-content.scss` — embedded chatbot widget
- `_endurancecalculator.scss` — SSD endurance calculator
- `_tcocalculator.scss` — total cost of ownership calculator
- `_toolsTcoEndurance.scss` — composite tools page
- `_filter-bar.scss` — search filter
- `_globalSearchResults.scss` — search results page
- `_pagination.scss` — molecule wrapper
- `_profileBadge.scss` — user profile UI
- `_search-bar.scss` — search input
- `_subscribeToEmail.scss` — replaces storybook's `_newsletter.scss`
- `_textSummary.scss` — text summary block

**Themes (1 new):**
- `theme-gray-mid` — additional `$gray-mid` (#52514f) background variant

**Component evolution (Button atom):**
- AEM uses `<img>` element with a `.btn-icon` CSS class instead of storybook's CSS-only `::after` SVG pseudo-element
- This is a maintainability improvement (AEM authors can swap icons in CMS without SCSS changes)

### 3.2 Storybook Has That AEM Doesn't

**Molecules (3):**
- `_membershipTiers.scss` — pricing/tier card layout
- `_newsletter.scss` — replaced by `_subscribeToEmail.scss` in AEM
- `_officeMap.scss` — different filename casing (AEM has `_officemap.scss`)
- `_contentSearch.scss` — exists as molecule (promoted to atom in AEM)

### 3.3 Known Bugs

| Bug | Storybook | AEM |
|-----|-----------|-----|
| `#21201e` typo in gradient theme (off-by-1 from `$gray-dark` `#21201f`) | ✅ Fixed → uses `$gray-dark` | ❌ **Still has the bug** |

---

## 4. Component Diff Summary

Of 47 SCSS files present in both repos:

- **0 files** have foundation/token-level differences
- **~30 files** have minor implementation evolution (hover states, accessibility, AEM-specific class naming, refactored variable naming)
- **~17 files** are identical or near-identical

The diffs are **implementation drift**, not **design drift**. Both repos visually render the same design language.

---

## 5. Atom Inventory Comparison

| Atom | Storybook | AEM | Notes |
|------|-----------|-----|-------|
| Alert | ✅ (story) | ✅ (molecule) | Different categorization |
| Breadcrumb | ✅ | ✅ | — |
| Button | ✅ | ✅ | AEM uses `<img>` icon pattern; Storybook uses CSS pseudo |
| Checkbox | ✅ (SCSS only, no story) | ✅ | Both have it |
| ContentBlock | ✅ | ✅ | — |
| ContentSearch | ✅ (in molecules) | ✅ (promoted to atom) | — |
| DownloadLink | ✅ | ✅ | — |
| Eyebrow | ✅ | ✅ | — |
| LinkItem | ✅ | ✅ | — |
| Modal | ✅ | ✅ | — |
| Pagination | ❌ | ✅ | AEM-only |
| ResponsiveImage | ✅ | ✅ | — |
| Text | ✅ | ✅ | — |

---

## 6. Implications for Canonical Tokens (this repo only)

The two web repos are **evidence**, not migration targets. This project's deliverable is a vendor-neutral token system in `tokens/` that any Solidigm surface (web, print, iOS, partner portal, internal tools, AI agents) can consume.

**What the evidence supports canonicalizing:**
- 16-color palette (already done) + 2 feedback colors (`interface-red`, `warning-red`)
- Sora (web) + Sequel100/Roboto (print/brand) as named contexts
- 4px-based spacing primitives — but cleaned of Bootstrap leftovers
- Modern breakpoints (640/768/1024/1280/1440) — not Bootstrap's 576/992
- Radius primitives reflecting the "sharp corners" brand rule (0 default)
- Shape language: 45° notch angle + named cut sizes
- Motion: 4–5 durations + standard easings (currently ad-hoc in CSS)
- Elevation: 4 shadow tiers (currently ad-hoc in CSS)

**What the evidence shows we should NOT canonicalize:**
- Component-specific pixel values (hero variant heights, navbar height, modal widths)
- Bootstrap leftovers (`28px`, `56px`, `88px` — no design rationale)
- Container max-widths that are site-specific (1920px is a marketing-site choice)
- AEM- or Storybook-specific class prefixes
- One-off `clip-path` polygons (those are derivations of the 45° rule)

### On the gradient typo (`#21201e`)

Both web repos contain `#21201e` in the gradient theme — off by one in the blue channel from `$gray-dark` (#21201f). Almost certainly a typo. We will NOT propagate it. Canonical token = `$gray-dark`. If web teams later choose to align, the canonical value is here.

### On the Storybook/AEM divergence (gray-mid theme, Button icon pattern, etc.)

These are downstream implementation choices. They don't affect canonical tokens. We capture them as evidence but don't mirror them.

---

## 7. Proposed Token Architecture (this repo)

```
tokens/
├── primitives/         ← Tier 1: pure brand language
│   ├── color.json      (16 colors + 2 feedback)
│   ├── typography.json (Sora web + Sequel100/Roboto print)
│   ├── space.json      (4px grid: 1=4, 2=8, ... 24=96 — clean, no Bootstrap leftovers)
│   ├── radius.json     (none=0, sm=4px, pill=9999px, circle=50%)
│   ├── shape.json      (notch-angle: 45deg, cut sizes: sm/md/lg)
│   └── breakpoints.json (xs=0, sm=640, md=768, lg=1024, xl=1280, 2xl=1440)
│
├── semantic/           ← Tier 2: usage-driven aliases
│   ├── color.json      (surface.primary → purple, feedback.error → interface-red)
│   ├── space.json      (gap.sm=20, gap.md=30, gap.lg=40,
│   │                    section.sm=70, section.md=100, section.lg=150)
│   ├── motion.json     (duration.fast=200ms, base=300ms, slow=500ms;
│   │                    easing.standard, easing.emphasized)
│   └── elevation.json  (shadow.card, shadow.dropdown, shadow.overlay)
│
└── platform/           ← Tier 3: platform-specific extensions (optional)
    ├── web.json        (icon sizes, container widths, notch render dimensions)
    ├── print.json      (CMYK equivalents, point sizes)
    └── ios.json        (placeholder for future)
```

**Build outputs (Style Dictionary):**
- `dist/css/tokens.css`, `dist/scss/_tokens.scss`, `dist/js/tokens.js`
- `dist/figma/tokens.json` (Tokens Studio)
- `dist/swift/Tokens.swift`, `dist/android/tokens.xml` (future)

**Consumer model:** any surface (Storybook, AEM, Figma, future apps) can pull the format it needs. They are not required to migrate. The canonical values exist here, accessible to humans (via the docs site) and AI agents (via the MCP).

---

## 8. Risks if We Don't Build Canonical Tokens

1. **The MCP can't be authoritative.** `get_color` works because we copied colors here. If a downstream team changes a color in their SCSS, our MCP returns stale data. Same problem will compound for spacing/radius/motion.
2. **New surfaces can't onboard cleanly.** A future iOS app, partner portal, or print campaign has no single place to read "what is Solidigm." They'll either re-derive from a website (wrong abstraction) or invent values (drift).
3. **Figma keeps diverging.** The DS 3.0 file already lacks spacing/radius variables that the code has. Without canonical tokens, design tool and code can't reconcile.
4. **AI agents hallucinate.** Without `validate_brand_output` checks for spacing/radius/motion, agents will invent plausible-looking values that aren't on-brand.

---

## 9. Summary

| Question | Answer |
|----------|--------|
| Are Storybook and AEM the same design system? | **Yes** — same primitives, identical hex/font/spacing values, parallel implementations. |
| Should either be the brand-token authority? | **No** — both contain delivery-layer concerns (Bootstrap, AEM classes, component-specific values). |
| Where should canonical tokens live? | **Here** (`tokens/` in this repo), built to be consumed by any surface. |
| What's the format? | W3C DTCG JSON, built by Style Dictionary into CSS/SCSS/JS/Figma/Swift outputs. |
| What's the next step? | Draft `space`, `breakpoints`, `radius`, `shape`, `motion`, `elevation` token files + semantic aliases. |
