# Iconography

## Design Principles
Icons are derived from the DNA of the Solidigm logo:
- **45° and 90° angles** — all icons built on this grid
- **Single line weight** — no fills, no gradients
- **72px × 72px container** — icons should not protrude from this container
- Include a **brand corner** (90° inner angle, 45° outer angles) where possible
- Minimum size: 16px (screen) / 6mm (print)
- Maximum size: 200px (screen) / 75mm (print) — larger requires brand approval

## Icon Color Usage
- Primary: white or gray icons on brand purple backgrounds, with teal/orange accent if needed
- Secondary: white/gray on dark blue or dark gray backgrounds
- Light backgrounds allow both white and dark icons
- Do NOT use insufficient contrast combinations (e.g., light purple on purple)
- Do NOT overuse accent colors

## Icon Misuse
- Do not use more than one line weight in a single icon
- Do not add gradients
- Do not add additional elements to existing icons
- Do not overlap multiple icons
- Do not use icons inline with text
- Do not resize multiple icons to different sizes in the same set

---

## UI Atom Icons

These are canonical interactive icons — not general-purpose icon library icons. They are brand primitives that appear on every Solidigm digital surface. Full path data, size bindings, and animation specs live in [`tokens/icons.json`](../tokens/icons.json). SVG files are in [`brand/assets/icons/`](assets/icons/).

### Double Arrow — Navigation / Link Icon

The most frequently appearing interactive icon on solidigm.com. Two right-pointing chevrons signal navigation: "go further, learn more."

| Property | Value |
|----------|-------|
| **Asset** | `brand/assets/icons/arrow-double.svg` (currentColor) |
| **Asset (CTA)** | `brand/assets/icons/arrow-double-teal.svg` (Electric Teal, 24×24) |
| **ViewBox (link)** | `0 0 40 27` |
| **ViewBox (button)** | `0 0 24 24` |
| **Dark theme fill** | White (`#FFFFFF`) — inherited via `currentColor` |
| **Light theme fill** | Black (`#000000`) — inherited via `currentColor` |
| **Button/CTA fill** | Electric Teal (`#00FFEC`) — always, on dark/purple backgrounds |
| **Size (mobile)** | 24×24px (`icon.size.sm`) |
| **Size (desktop)** | 32×32px (`icon.size.md`) at ≥1280px |

#### Hover Animation — Two simultaneous effects

1. **Icon nudge:** Container translates `translateX(4px)` — `300ms ease-in-out`
2. **Underline expand:** Text `span::before` animates `width: 0% → 100%` — `300ms ease-in-out`
   - Dark theme underline: white
   - Light theme underline: black
   - Offset: `-2px` mobile / `-10px` desktop

#### When to use each variant

| Context | Asset | Fill |
|---------|-------|------|
| List items, link cards, navigation rows | `arrow-double.svg` | currentColor |
| `.text--arrow` CSS utility (text decoration) | CSS mask-image | `background-color` (default: Solidigm Purple) |
| Primary buttons, CTAs | `arrow-double-teal.svg` | Electric Teal |
| Modal navigation | `arrow-double-teal.svg` | Electric Teal |

---

### Accordion Chevron — Toggle Icon

Used exclusively in accordion trigger buttons. Points down (closed) and rotates 180° when expanded.

| Property | Value |
|----------|-------|
| **Asset** | `brand/assets/icons/chevron-down.svg` |
| **ViewBox** | `0 0 27 14` |
| **Fill** | Electric Teal (`#00FFEC`) — **always, not theme-adaptive** |
| **Size (mobile)** | 16×16px (`icon.size.xs`) |
| **Size (desktop)** | 24×24px (`icon.size.sm`) at ≥1024px |

#### Toggle Animation

- **Closed → Open:** `rotate(0deg) → rotate(180deg)` — `500ms ease-in-out`
- **Content reveal:** `max-height`, `opacity`, `padding` all transition at `500ms`

> **Brand note:** The Electric Teal fill on the accordion chevron is a hardcoded brand constant — it does not invert on light themes. Accordion components are always used on dark or purple backgrounds.

