# Platform Override: Web (Dotcom / AEM / Marketing)

Applies to: solidigm.com, AEM corporate site, marketing landing pages, campaign microsites.

---

## Typography

| Context | Font | Weights | Fallback |
|---------|------|---------|----------|
| All headings (H1–H6) | Sora ExtraLight / SemiBold | 200, 600 | `sans-serif` |
| Body, captions, labels | Sora Regular / Medium | 400, 500 | `sans-serif` |
| Code / mono | Roboto Mono | 400 | `monospace` |

- Load via `@font-face` or Google Fonts CDN. Sora must load before first contentful paint.
- Fluid type: clamp() from mobile breakpoint (640px) to desktop (1440px). See `tokens/typography.json`.
- Sequel100 is **not used** on web — print/brand collateral only.

---

## Color

- **Dark theme (`theme-solidigm--dark`):** dark background, white text, Electric Teal accents
- **Light theme (`theme-solidigm--light`):** white background, black text, purple or teal accents
- **Purple theme (`theme-solidigm--purple`):** Solidigm Purple background
- **Ultra Dark Purple theme (`theme-solidigm--ultra-dark-purple`):** darkest brand surface

Token path: `{Dark.Solidigm Purple}`, `{Accents.Electric Teal}`, etc.  
CSS classes applied to section wrappers — never per-component.

---

## Icons

| Icon | Asset | Fill rule |
|------|-------|-----------|
| Link / navigation arrow | `brand/assets/icons/arrow-double.svg` | `currentColor` — white (dark) / black (light) |
| Button / CTA arrow | `brand/assets/icons/arrow-double-teal.svg` | `#00FFEC` always |
| `.text--arrow` utility | CSS `mask-image` data URI | `background-color` (default: Solidigm Purple) |
| Accordion chevron | `brand/assets/icons/chevron-down.svg` | `#00FFEC` always |

Icon sizes: `icon.size.xs` (16px) → `icon.size.md` (32px). See `tokens/icons.json`.

---

## Notch / Shape

- The 45° notch is the primary geometric brand element on web.
- Applied via `clip-path: polygon(...)` — see `tokens/shape.json` for all four corner variants.
- Hero sections always use the notch. Cards use it sparingly (feature cards only).

---

## Spacing & Layout

- Base grid: 4px. All spacing from `tokens/space.json`.
- `$gap-mobile` = 30px (`space.7`), `$gap-desktop` = 40px (`space.10`).
- Container max: 1920px. Design artboard: 1440px. See `tokens/breakpoints.json`.
- Breakpoints: `sm=640, md=768, lg=1024, xl=1280, 2xl=1440`.

---

## Motion

- Default interaction: `motion.base` (300ms) + `motion.easing.standard`.
- Accordion open/close: `motion.slow` (500ms) + `motion.easing.emphasized`.
- Respect `prefers-reduced-motion` — disable all transitions when set.

---

## Accessibility

- WCAG 2.1 AA minimum. AA+ (7:1) preferred for body text on brand purple.
- All interactive elements keyboard navigable.
- SVG icons: `aria-hidden="true"` when decorative; `role="img"` + `<title>` when meaningful.
- Accordion: `aria-expanded`, `aria-controls` on trigger button.

---

## Do Nots

- Do not use Bootstrap spacing values (28px, 56px, 88px) — use the 4px grid.
- Do not use `border-radius` without a reason — sharp corners are the default.
- Do not hardcode hex values — reference `tokens/colors.json`.
- Do not use Sequel100 or Roboto for headings — Sora only on web.
