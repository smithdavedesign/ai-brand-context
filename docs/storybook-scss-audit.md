# Storybook SCSS — Evidence for Canonical Tokens

> **Date:** 2026-04-25
> **Source (read-only reference):** `enterprise_apps.marketing.application.solidigm_com_storybook`
> **Purpose:** Evidence-gathering for designing canonical, vendor-neutral brand tokens in this repo. The Storybook repo is **not** a target for changes — it's an input that shows how the brand is currently expressed in marketing-site code.
> **Status:** Read-only. No edits will be made to the Storybook repo from this project.

---

## 1. Architecture Overview

```
main.scss                          ← Root entry point
├── base/_bootstrapOverrides.scss  ← $spacer, breakpoints, spacer map, padding/gap vars
│   └── bootstrap/scss/mixins      ← Bootstrap 5.3.8 mixins
├── .theme-solidigm
│   ├── base/main.scss
│   │   ├── _colors.scss           ← 21 SCSS vars + $colors map
│   │   ├── _mixins.scss           ← Button, transition, box-shadow, theme, vw/vh helpers
│   │   ├── _reset.scss            ← normalize.css v8.0.1
│   │   ├── _typography.scss       ← Font sizes, line-heights, fluid-clamp(), type classes
│   │   ├── _theme.scss            ← 6 theme variants (light/dark/purple/ultra-dark/gray-dark/gradient)
│   │   └── _base.scss             ← Utility classes (gap, padding, margin, display, alignment)
│   ├── containers/main.scss
│   │   ├── _containers.scss       ← Grid, clip-paths, .cmp-containers
│   │   └── _containerwithimage.scss ← Background image/video containers
│   ├── atoms/main.scss
│   │   ├── _buttons.scss          ← 7 button variants + tertiary
│   │   ├── _checkboxes.scss       ← form-check component
│   │   ├── _eyebrow.scss          ← Simple flex layout
│   │   └── _modal.scss            ← Dialog/modal layout
│   └── molecules/main.scss
│       └── 43 component files     ← All layout-level components
```

---

## 2. Foundation Variables (from `_bootstrapOverrides.scss`)

### 2.1 Base Spacer

```scss
$spacer: 1rem;  // = 16px (browser default)
```

**Everything is built on this single unit.** Most values are `$spacer * N`.

### 2.2 Breakpoints

| Token | Value | Usage |
|-------|-------|-------|
| `xs` | `0` | Default / mobile-first |
| `sm` | `576px` | Small mobile |
| `md` | `768px` | Tablet |
| `lg` | `992px` | Laptop / desktop threshold |
| `xl` | `1280px` | Desktop |
| `xxl` | `1440px` | Wide desktop (mock width) |

Storybook preview viewports: Mobile `393×800`, Tablet `768×1024`, Laptop `1280×1024`.
Max content width: `1920px`. Mock artboards designed at `1440px`, scaled to `1920px` via `vwDesktop()`.

### 2.3 Spacer Scale ($spacers map)

| Key | Multiplier | Computed |
|-----|-----------|----------|
| 0 | 0 | 0 |
| 1 | 0.25 | 4px |
| 2 | 0.5 | 8px |
| 3 | 0.75 | 12px |
| 4 | 1 | 16px |
| 5 | 1.25 | 20px |
| 6 | 1.5 | 24px |
| 7 | 1.75 | 28px |
| 8 | 2 | 32px |
| 9 | 2.5 | 40px |
| 10 | 3 | 48px |
| 11 | 3.5 | 56px |
| 12 | 4 | 64px |
| 13 | 4.5 | 72px |
| 14 | 5 | 80px |
| 15 | 5.5 | 88px |
| 16 | 6 | 96px |

### 2.4 Semantic Spacing Variables

| Variable | Multiplier | Computed | Purpose |
|----------|-----------|----------|---------|
| `$gap-mobile` | 1.875 | **30px** | Primary mobile gap |
| `$gap-desktop` | 2.5 | **40px** | Primary desktop gap |
| `$gap-20` | 1.25 | **20px** | Secondary gap |
| `$padding-mobile` | 4.375 | **70px** | Section padding mobile |
| `$padding-tablet` | 6.25 | **100px** | Section padding tablet |
| `$padding-desktop` | 9.375 | **150px** | Section padding desktop |
| `$container-padding-x` | 1 | **16px** | Container inline padding |

### 2.5 Inline Padding Map ($inlinePaddings)

| Breakpoint | Value | Purpose |
|------------|-------|---------|
| `lg` | `32px` | Container inner padding at lg |
| `xl` | `40px` | Container inner padding at xl |
| `xxl` | `80px` | Container inner padding at xxl |

### 2.6 Column Space Map ($column-space)

| Breakpoint | Multiplier | Computed |
|------------|-----------|----------|
| `sm` | 1.25 | 20px |
| `md` | 2.5 | 40px |
| `lg` | 4.375 | 70px |
| `xl` | 6.25 | 100px |
| `xxl` | 9.375 | 150px |

### 2.7 Padding Map ($padding-map, in `_base.scss`)

| Key | Value |
|-----|-------|
| `xs` | 30px |
| `sm` | 40px |
| `md` | 70px |
| `lg` | 100px |
| `xl` | 150px |

### 2.8 Icon Sizes ($iconSize)

| Key | Computed |
|-----|----------|
| `xs` | 16px |
| `sm` | 24px |
| `md` | 32px |
| `lg` | 48px |
| `xl` | 64px |

### 2.9 Grid

```scss
$grid-columns: 12;
$grid-gutter-width: 1.25rem;  // 20px
$grid-row-columns: 6;
$enable-negative-margins: true;
```

### 2.10 Max Width

```scss
--max-width: 1920px;           // CSS custom property
$max-width-image-tablet: $spacer * 29.6875;  // 475px
```

---

## 3. Border Radius

| Value | Where Used |
|-------|-----------|
| **`0`** | Buttons (`.btn { border-radius: 0 }`) — **explicitly zero, sharp corners** |
| **`4px`** | Navbar search input (`_navbar.scss:696`) |
| **`50%` / `100%`** | Circular elements only: play buttons, milestone dots, social icons, video overlays, close buttons |
| **`100px`** | Carousel progress bars (`_carousel.scss:210`) — pill shape |
| **`0.5rem` (8px)** | `$border-radius-sm` — Bootstrap override, not directly used in component CSS |
| **`1rem` (16px)** | `$border-radius-lg` — Bootstrap override, not directly used in component CSS |

**Key finding:** The design system is almost entirely **zero-radius** (sharp geometric). The only non-circular radius values are `4px` (navbar search) and `100px` (carousel pill).

---

## 4. Box Shadows

| Shadow Value | Components |
|-------------|-----------|
| `0 4px 4px 0 rgba(0,0,0,0.25)` | Dropdown, Tabs, Content Hub |
| `0 4px 4px 0 rgba(0,0,0,0.5)` | Tabs (dark variant) |
| `0 4px 20px rgba(0,0,0,0.1)` | Office Map card |
| `0px 16px 40px 20px rgba($white, 0.16)` | Cookie Preferences |
| `0 -2px 0 0 $purple` | Content Hub active tab (inset effect) |

**Key finding:** Very sparse shadow usage. Only 4 unique shadow patterns across the entire system.

---

## 5. Transitions

### 5.1 Common Durations

| Duration | Easing | Usage |
|----------|--------|-------|
| **0.2s** | `ease`, `ease-in-out` | Button arrow, navbar show/hide, checkbox, milestone |
| **0.3s** | `ease`, `ease-in-out`, `linear` | Most component interactions (accordion, dropdown, cards, hero, navbar, search, tabs, industry solutions, content hub) |
| **0.4s** | `ease-in` | Navbar chevron rotation |
| **0.5s** | `ease-in-out`, `ease-in` | Accordion open/close, hero filter, product list, specification overview |
| **0.6s** | `linear` | Button loader spin |
| **0.8s** | `ease`, `cubic-bezier(0.4,0,0.2,1)` | Customer logo carousel |
| **1s** | (opacity) | Sticky scroll fade |
| **1.8s** | `ease-in-out` | Hero featured image transform |

### 5.2 Common Patterns

- **Arrow translate:** `transform: translateX(4px)` on hover — buttons, cards, link items
- **Chevron rotation:** `transform: rotate(180deg)` — accordion, dropdown, tabs
- **Underline grow:** `width: 0 → 100%` — footer links, link items, spec overview
- **Scale on hover:** `transform: scale(1.2)` — industry solutions
- **Fade in/out:** `opacity 1000ms` — sticky scroll sections

---

## 6. Component-Level Spacing Catalog

### 6.1 Buttons (atom)

| Property | Mobile | Desktop |
|----------|--------|---------|
| `padding` | `16px 28px` | `18px 28px` |
| `min-width` | `225px` ($spacer*14.0625) | `276px` ($spacer*17.25) |
| `border-radius` | `0` | `0` |
| `border` | `1px solid` | `1px solid` |
| Tertiary arrow | `24×24px` icon, `6px` margin-left | same |
| Loader | `16×16px` | same |

### 6.2 Checkboxes (atom)

| Property | Value |
|----------|-------|
| `height` | `54px` |
| `gap` | `10px` |
| Checkmark | `13×13px` (unchecked) / `15×13px` (checked) |
| `border` | `1px solid` |

### 6.3 Eyebrow (atom)

| Property | Value |
|----------|-------|
| `gap` | `10px` ($spacer*0.625) |

### 6.4 Modal (atom)

| Property | Mobile | Desktop |
|----------|--------|---------|
| Dialog max-width | `1098px` ($spacer*68.625) | same |
| Header padding | `20px` | same |
| Content padding | `20px` | same |
| Content row-gap | `30px` | `20px` (2-column grid) |
| Content max-height | `80vh` | `60vh` |
| Footer gap | `16px` | same |
| Footer button max-width | `160px` | same |
| Close button height/width | `30×30px` | `40×40px` |

### 6.5 Accordion (molecule)

| Property | Mobile | Desktop |
|----------|--------|---------|
| Inter-item margin-top | `30px` ($gap-mobile) | `40px` ($gap-desktop) |
| Content margin-bottom | `30px` | `20px` ($gap-desktop*0.5) |
| Open content gap | `30px` | `40px` |
| Padding-top (open) | `30px` | `40px` |
| Chevron icon | `16px` (xs) | `24px` (sm) |
| Nested accordion padding-right | — | `40px` |
| Image max-width | `475px` ($max-width-image-tablet) | `min(80%, 573px)` |
| Row-gap in grid | `30px` | — |
| Column-gap | — | `20px` |
| Sub-item gap | `20px` | same |

### 6.6 Hero (molecule)

| Property | Mobile | Desktop |
|----------|--------|---------|
| Padding-block | `70px` ($padding-mobile) | `40px` ($gap-desktop) |
| Min-height (Large) | `590px` | `1080px` |
| Min-height (Medium) | `492px` | `810px` |
| Min-height (Small) | `393px` | `540px` |
| Min-height (Full) | `100vh` | `100vh` |
| Content gap | `30px` | `40px` |
| CTA gap | `20px` | same |
| Background max-width | `2400px` ($spacer*150) | same |
| Featured image max-width | `475px` | `1320px` ($spacer*82.5) |
| Featured image max-height | — | `720px` ($spacer*45) |
| Featured transform | — | `translateY(192px)` ($spacer*12) |
| Play button | `64×64px` | `vwDesktop(124)` ≈124px |
| Play button border | `8px solid $white` | same |
| Video hero padding-bottom | `96px` | `176px` |
| Video hero margin-top | `70px` | `150px` |
| Featured product hero width | — | `min(41%, 722px)` |

### 6.7 Navbar (molecule)

| Property | Mobile | Desktop |
|----------|--------|---------|
| Height | `58px` ($spacer*3.625) | `92px` ($spacer*5.75) |
| Logo max-width | `156px` ($spacer*9.75) | `192px` ($spacer*12) |
| Menu gap | `30px` ($gap-mobile) | `vwDesktop(70)` |
| Submenu padding | `20px` | `0` |
| Nav link gap | `8px` | `8px` |
| Chevron | `16×16px` | same |
| Mobile menu padding-block | `40px 60px` | — |
| Mega menu gap | — | `40px` ($gap-desktop) |
| Mega menu padding-left | — | `calc(2rem+12rem+vwDesktop(70))` |
| Search dropdown border-radius | — | `4px` |
| Search max-height | — | `290px` |

### 6.8 Cards (molecule)

| Property | Mobile | Desktop |
|----------|--------|---------|
| Padding-bottom | `30px` | `40px` |
| Icon size | `48×48px` | `62×62px` |
| Outlined card padding | `30px` | `40px` |
| Divider margin-block | `20px` | `30px` |
| Content gap | `20px` | same |
| Card link gap | `30px` | `vwDesktop(70)` |
| Arrow icon | `24×24px` | `32×32px` |
| Description gap | `20px` | same |
| Product badge | `64×64px` | same |
| Stat card padding | `30px 20px` | `30px 40px` |
| Card border | `0.5px solid` | same |

### 6.9 Breadcrumb (molecule)

| Property | Mobile | Desktop |
|----------|--------|---------|
| Padding-inline | `20px` | responsive ($inlinePaddings) |
| Padding-top | `12px` ($spacers[3]) | same |
| Padding-bottom | `12px` | `24px` |
| Separator width | `1px` | same |
| Separator height | `11.2px` ($spacer*0.7) | same |
| Max-width | `1920px` | same |
| Margin-bottom | `16px` | same |

### 6.10 Footer (molecule)

Large component with many sub-elements. Key spacing:

| Property | Mobile | Desktop |
|----------|--------|---------|
| Section padding-bottom | `40px` ($gap-desktop) | `70px` ($padding-mobile) |
| Social icons gap | `32px` | `24px` |
| Social icon size | `32×32px` | `24×24px` |
| Logo max-width | `277px` | `252px` |
| Link group gap | `16px` | `20px` |
| Top section margin-top | `70px` | `150px` or `136px` |
| Bottom bar padding-block | `20px` | `40px` |
| Accordion divider height | `8px` | same |
| Notch (with image) | `128×128px` | `357×357px` |
| Notch (no image) | `128×128px` | `190×190px` |
| VIP section margin-top | `105px` | same |

### 6.11 Carousel (molecule)

| Property | Mobile | Desktop |
|----------|--------|---------|
| Max-width | `1920px` | same |
| Progress bar height | `6px` | `8px` |
| Progress bar border-radius | `100px` | same |
| Progress bar max-width | `84px` ($spacer*5.25) | `max(6.5vw, 48px)` |
| Indicator gap | `3px` | `8px` |
| Indicator min-width | — | `78px` |
| Padding-bottom (dots area) | `8px` | `16px` |
| Slide padding-bottom (with dots) | `50px` | same |

### 6.12 Bento Box (molecule)

| Property | Mobile | Desktop |
|----------|--------|---------|
| Cell padding | `20px` | `40px` |
| Cell gap | `30px` | `40px` |
| Notch dimension | `96px` | `146px` |
| Notch tablet | `100px` | — |
| Arrow icon | `24×24px` | `32×32px` |
| Arrow position | `20px` from edges | `40px` from edges |
| Divider height | `2px` | same |

### 6.13 Blade (molecule)

| Property | Mobile | Desktop |
|----------|--------|---------|
| Content gap | `30px` | same |
| Image max-width | — | `475px` |
| Bleed margin | `-20px` | responsive ($inlinePaddings) |

### 6.14 Content Block / Content Hub

| Property | Mobile | Desktop |
|----------|--------|---------|
| Tag pill padding | `14px` inline, `8px` block | `20px` inline |
| Filter dropdown shadow | `0 4px 4px 0 rgba(0,0,0,0.25)` | same |
| Active tab indicator | `0 -2px 0 0 $purple` | same |

### 6.15 Key Features (molecule)

| Property | Mobile | Desktop |
|----------|--------|---------|
| Row-gap | `60px` | `30px` |
| Feature gap | `40px` | `10px` |
| Bullet size | `11×11px` | same |
| Gap between bullet/text | `18px` | same |
| Image max-width | `475px` | `83%` |

### 6.16 Customer Story (molecule)

| Property | Mobile | Desktop |
|----------|--------|---------|
| Content gap | `30px` | `40px` |
| Internal gap | `32px` | `96px` |
| Quote logo max-width | — | `320px` |
| Overlap margin-top | — | `-50px` |

### 6.17 Newsletter (molecule)

| Property | Mobile | Desktop |
|----------|--------|---------|
| Padding-block | `40px` | same |
| Input padding | `10px 16px` | `0 0 0 30px` |
| Input border-bottom | `1px solid` | `none` |
| Input height | — | `94px` |
| Submit icon | `24×16px` | same |
| Success icon | `32×32px` | same |
| Submit button | — | `276px × 54px` |

### 6.18 Sticky Scroll (molecule)

| Property | Mobile | Desktop |
|----------|--------|---------|
| Section padding-block | `70px` | `0` then `150px top` |
| Content gap | `30px` | `40px` |
| Content margin-bottom | `70px` | `150px` |
| Play button | `64×64px`, `8px border` | same |
| Fallback padding-bottom | `70px` | same |

### 6.19 Tabs (molecule)

| Property | Mobile | Desktop |
|----------|--------|---------|
| Tab gap | `24px` | `24px` |
| Tab padding-block | `25px` | `20px` |
| Active indicator height | `4px` | same |
| Active indicator width | `239px` | same |
| Dropdown max-height | `300px` | same |
| Dropdown shadow | `0 4px 4px 0 rgba(0,0,0,0.25)` | same |
| Dropdown item padding | `14px 20px` | same |

### 6.20 Product Cards (molecule)

| Property | Mobile | Desktop |
|----------|--------|---------|
| Card padding | `50px 20px 20px` | `50px 40px` |
| Badge clip | `112×112px` | same |
| Separator margin | `20px 0` | same |
| Feature gap | `20px` | same |
| Border | `1px solid` | same |

### 6.21 Product List (molecule)

| Property | Mobile | Desktop |
|----------|--------|---------|
| Filter height | `54px` ($spacer*3.375) | same |
| Filter gap | `10px` | same |
| List gap | `30px` | `40px` |
| Product image | `48×84px` → `68×84px` | `104×128px` |
| Dropdown max-height | `315px` | same |

### 6.22 Industry Solutions (molecule)

| Property | Mobile | Desktop |
|----------|--------|---------|
| Max-width | `2400px` | same |
| Min-height | `382px` | `600px` |
| Content padding | `20px` | `40px` |
| Image size | — | `vwDesktop(722) × vwDesktop(460)` |
| Arrow icon | `24×24px` | `32×32px` |

### 6.23 By The Number (molecule)

| Property | Mobile | Desktop |
|----------|--------|---------|
| Section gap | `70px` | same |
| Card gap | `20px` | `30px` |
| Card max-width | — | `379px` |
| Card border-radius | `50%` (circular) | same |
| Card border | `1px solid` | same |

### 6.24 Specification Overview (molecule)

| Property | Value |
|----------|-------|
| `$spec-spacing-standard` | `20px` ($spacer*1.25) |
| `$spec-spacing-small` | `10px` ($spacer*0.625) |
| Dropdown max-width | `220px` |
| Filter height | `54px` |
| Media max-width | `312px` ($spacer*19.5) |
| Table row padding-block | `20px` |
| Button min-width | `225px` |
| Button height | `54px` |

### 6.25 Office MAP (molecule)

| Property | Value |
|----------|-------|
| Total height | `830px` (min + max) |
| Background max-width | `150rem` (2400px) |
| Card max-width | `353px` → `425px` (desktop) |
| Card padding | `20px` |
| Card gap | `20px` |
| Card shadow | `0 4px 20px rgba(0,0,0,0.1)` |
| Border | `2px solid currentColor` |

### 6.26 Milestone (molecule)

| Property | Mobile | Desktop |
|----------|--------|---------|
| Item margin-bottom | `30px` | `0` |
| Timeline dot | `10×10px` | same |
| Timeline line width | `2px` | same |
| Content padding-left | `38px` | `0` |
| Content gap | `20px` | same |
| Image max-width | `510px` | same |

### 6.27 Other Components (select notable values)

| Component | Property | Mobile | Desktop |
|-----------|----------|--------|---------|
| **Alert** | padding-block | `10px` | `20px` |
| **Alert** | padding-inline | `20px` | `30px` |
| **Alert** | icon | `24×24px` | `32×32px` |
| **Button Group** | gap | `20px` | same |
| **Column Container** | padding-inline | `20px` | responsive |
| **Column Container** | column-gap | `20px` | same |
| **Column Container** | row-gap | `30px` | same |
| **Compare Overlay** | max-width | `576px` | same |
| **Cookie Prefs** | max-width | `716px` | same |
| **Customer Logo** | logo height | `24px` | `32px` |
| **Customer Logo** | logo max-width | `200px` | `300px` |
| **Dropdown** | padding | `20px` | same |
| **Dropdown** | max-height | `290px` | same |
| **Dropdown** | item padding | `14px 20px` | `14px 20px` |
| **Link Item** | gap | `24px` | `30px` |
| **Media List** | row-gap | `30px` | `40px` |
| **Media List** | image max | `510×245px` | same |
| **PDP Tabs** | top (sticky) | `57px` | `92px` |
| **Support List** | section gap | `150px` | same |

---

## 7. Container System

### 7.1 Container Widths

| Element | Max-Width |
|---------|----------|
| `.cmp-containers` | `1920px` |
| Background images | `2400px` ($spacer*150) |
| Content | `2400px` |
| Carousel | `1920px` |
| Navbar content | `1920px` |

### 7.2 Notch / Clip-Path Dimensions

| Context | Mobile | Tablet | Desktop |
|---------|--------|--------|---------|
| BentoBox | `96px` | `100px` | `146px` |
| Container inside | `96px` | `100px` | `146px` |
| Footer (with image) | `128px` | — | `357px` |
| Footer (no image) | `128px` | — | `190px` |

---

## 8. Themes

6 themes, all define `background-color` and `* { color }`:

| Theme Class | Background | Text | Icon Fill |
|-------------|-----------|------|-----------|
| `--light` | `$white` | `$black` | `$purple` |
| `--dark` | `$black` | `$white` | `$accent-teal` |
| `--purple` | `$purple` | `$white` | `$accent-teal` |
| `--ultra-dark-purple` | `$purple-ultra-dark` | `$white` | `$accent-teal` |
| `--gray-dark` | `$gray-dark` | `$white` | `$accent-teal` |
| `--gradient` | `linear-gradient(0deg, #000 7.5%, #21201e 29%, #000 100%)` | `$white` | `$accent-teal` |

---

## 9. Colors (complete set from `_colors.scss`)

| Variable | Hex | In tokens/colors.json? |
|----------|-----|----------------------|
| `$purple` | `#4f00b5` | ✅ Solidigm Purple |
| `$purple-light` | `#8d59cf` | ✅ Purple Light |
| `$purple-dark` | `#2f006b` | ✅ Purple Dark |
| `$purple-ultra-dark` | `#160231` | ✅ Ultra Dark |
| `$blue-dark` | `#00083f` | ✅ Blue Dark |
| `$white` | `#ffffff` | ✅ White |
| `$white-light` | `#f4f3f1` | ✅ Warm White |
| `$gray` | `#a5a29d` | ✅ Medium Gray |
| `$gray-light` | `#f5f3f1` | ✅ Light Gray |
| `$gray-mid` | `#52514f` | ✅ Mid Gray |
| `$gray-dark` | `#21201f` | ✅ Dark Gray |
| `$black` | `#000000` | ✅ Black |
| `$accent-teal` | `#00ffec` | ✅ Electric Teal |
| `$pink` | `#ea11bc` | ✅ Pink |
| `$accent-orange` | `#ffa42c` | ✅ Orange |
| `$interface-red` | `#ba3640` | ❌ Not in tokens |
| `$warning-red` | `#ff0000` | ❌ Not in tokens |
| `$none` | `transparent` | — (utility) |

> **Note:** `$interface-red` and `$warning-red` are candidates for a future `color.semantic` or `color.feedback` group.

**Note on gradient theme:** `_theme.scss` contains `#21201e` in the gradient — off by one in the blue channel from `$gray-dark` (#21201f). Almost certainly a typo. We will NOT canonicalize that hex; canonical token = `$gray-dark`.

**Delta:** Storybook has 2 extra colors not in our tokens: `$interface-red` (#ba3640) and `$warning-red` (#ff0000).

---

## 10. Typography Summary

### Font
- **Family:** `Sora` (Google Fonts, weights 100–800)
- **Note:** Our tokens say `Sequel100`. Storybook uses `Sora`. These are different fonts.

### Weight Scale

| Name | Value |
|------|-------|
| `extralight` | 200 |
| `light` | 300 |
| `regular` | 400 |
| `medium` | 500 |
| `semibold` | 600 |
| `bold` | 700 |

### Fluid Typography

```scss
@function fluid-clamp($min-size, $max-size, $min-vw: 36, $max-vw: 90)
```

Viewport range: 576px → 1440px. Used for Hero, H1, H2, H3, H4, Accordion headings.

### Viewport-Relative Sizing

```scss
@function vwMobile($pixels)  // based on 393px viewport
@function vwDesktop($pixels) // based on 1920px viewport (scaled from 1440px mocks)
```

---

## 11. Storybook Atoms (complete list)

| Atom | SCSS file | Notes |
|------|-----------|-------|
| **Alert** | (in molecules SCSS) | Notification banner, icon + text |
| **Breadcrumb** | (responsive inline padding) | Uses `$inlinePaddings` mixin |
| **Button** | `atoms/_buttons.scss` | 5 style variants (Primary Purple, Secondary Purple, Primary White, Secondary White, Tertiary) + video/modal behaviors |
| **ContentBlock** | (typography + base utils) | Text composition atom |
| **ContentSearch** | (dropdown + form) | Search input with suggestions dropdown |
| **DownloadLink** | (link item styles) | Anchor with file-type icon |
| **Eyebrow** | `atoms/_eyebrow.scss` | Label + rule, flex-column, 10px gap |
| **LinkItem** | (no dedicated SCSS) | Arrow link, typography + transition |
| **Modal** | `atoms/_modal.scss` | Full dialog: trigger, overlay, header/content/footer |
| **ResponsiveImage** | (no SCSS) | `<picture>` wrapper, Contentful image CDN |
| **Text** | (typography classes) | Body, caption, type-style wrappers |

> Only 4 atoms have dedicated SCSS: `_buttons`, `_checkboxes`, `_eyebrow`, `_modal`. The rest rely on base typography and layout utilities. **Checkboxes** exist as SCSS but have no Story — they're used via the Filter/ProductList molecules.

---

## 12. Key Patterns & Recurring Values

### 11.1 Most Frequently Used Spacing Values

From analyzing 1500+ spacing declarations:

| Value | Frequency | Description |
|-------|-----------|-------------|
| **`20px`** | ★★★★★ | Universal small gap/padding ($spacer*1.25 or $gap-20) |
| **`30px`** | ★★★★★ | Primary mobile gap ($gap-mobile) |
| **`40px`** | ★★★★★ | Primary desktop gap ($gap-desktop) |
| **`16px`** | ★★★★ | Base spacer ($spacer) |
| **`10px`** | ★★★★ | Tight gap ($spacer*0.625) |
| **`70px`** | ★★★ | Section padding mobile ($padding-mobile) |
| **`150px`** | ★★★ | Section padding desktop ($padding-desktop) |
| **`100px`** | ★★ | Section padding tablet ($padding-tablet) |
| **`24px`** | ★★ | $spacer*1.5 |
| **`8px`** | ★★ | $spacer*0.5 |
| **`4px`** | ★ | $spacer*0.25 |
| **`48px`** | ★ | $spacer*3 |
| **`64px`** | ★ | $spacer*4 |
| **`96px`** | ★ | $spacer*6 |
| **`12px`** | ★ | $spacer*0.75 |

### 11.2 Icon Size Progression

16 → 24 → 32 → 48 → 64 (matching the `$iconSize` map exactly)

### 11.3 Mobile → Desktop Patterns

Common responsive jumps:
- `30px → 40px` (gap)
- `70px → 150px` (section padding, with 100px tablet step)
- `24px → 32px` (icons)
- `48px → 62px` or `64px` (larger icons)
- `16px → 24px` (small icons)

---

## 13. What's Missing from Our Token Files

### Already tokenized:
- ✅ Colors (14 of 16 match; `interface-red` and `warning-red` missing)
- ✅ Typography (font sizes, line-heights — 28 styles)

### Needs tokenizing:

| Category | Priority | Proposed Token Count |
|----------|----------|---------------------|
| **Spacing scale** | 🔴 High | 17 values (spacers 0–16) |
| **Semantic spacing** | 🔴 High | 6 values (gap-mobile/desktop, padding-mobile/tablet/desktop, gap-20) |
| **Breakpoints** | 🔴 High | 6 values (xs through xxl) |
| **Icon sizes** | 🟡 Medium | 5 values (xs through xl) |
| **Border radius** | 🟡 Medium | 3 values (0, 4px, 50%) |
| **Box shadows** | 🟢 Low | 4 unique patterns |
| **Transition durations** | 🟢 Low | 4-5 common durations |
| **Container max-widths** | 🟢 Low | 3 values (1920, 2400, 475) |
| **Inline paddings** | 🟢 Low | 3 values (32, 40, 80px) |
| **Column space** | 🟢 Low | 5 values |
| **Missing colors** | 🟡 Medium | 2 (interface-red, warning-red) |

---

## 14. Open Questions for Discussion

1. **Font discrepancy:** Our tokens say `Sequel100` / `Roboto` / `Roboto Mono`. Storybook uses only `Sora`. Which is authoritative? Are these different contexts (marketing site vs. brand guidelines)?

2. **Gradient theme:** Uses hardcoded hex `#21201e` — is this the same as `$gray-dark` (#21201f)? Off-by-one in the blue channel.

3. **Interface colors:** Should `$interface-red` (#ba3640) and `$warning-red` (#ff0000) be added to the canonical token set, or are they implementation details?

4. **Viewport functions:** `vwMobile()` and `vwDesktop()` use magic reference widths (393 and 1920). Should these become tokens or remain implementation details?

5. **Component-specific values:** Many components define one-off pixel values (e.g., hero heights 590/492/393/1080/810/540). Should these be tokenized or left as component-level decisions?

6. **Notch dimensions:** Clip-path notch sizes (96/100/146px) are specific to the Solidigm design language. Are these tokens or just implementation details?

7. **Bootstrap dependency:** The spacer scale and grid system are Bootstrap 5 overrides. Should our tokens mirror Bootstrap's `$spacers` map exactly, or abstract away from it?

8. **Fluid typography:** The `fluid-clamp()` mixin generates responsive font sizes between 576px and 1440px. Our tokens have fixed mobile/desktop pairs. Should the token format include the clamp formula or just the endpoints?
