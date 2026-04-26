# Platform Override: iOS / Mobile Native

Applies to: Solidigm iOS apps, iPadOS apps, Swift UI components, React Native (iOS target).

---

## Typography

| Context | Font | Notes |
|---------|------|-------|
| Display / Hero headings | Sora ExtraLight (200) | Loaded as custom font via `UIFont` / SwiftUI `.custom()` |
| Subheadings, labels | Sora SemiBold (600) | |
| Body, secondary | SF Pro Text (system) | Fall back to system font for body — improves legibility at small sizes |
| Monospace / code | SF Mono (system) | |

- Sora must be bundled as a custom font resource (`.ttf`). Download from `brand/assets/fonts/` or Google Fonts.
- Never substitute Sequel100 on iOS — it is a print-only typeface.
- Dynamic Type: Sora custom fonts do not scale with iOS Dynamic Type by default. Implement `UIFontMetrics` scaling where possible.
- Minimum tap target font: 15pt / 20px equivalent.

---

## Color

- Follow the same token palette as web (`tokens/colors.json`).
- Dark mode: map `theme-solidigm--dark` → `UIUserInterfaceStyle.dark`.
- Light mode: map `theme-solidigm--light` → `UIUserInterfaceStyle.light`.
- Use `UIColor(dynamicProvider:)` or SwiftUI `Color` environment values to switch.

| Token | Dark mode hex | Light mode hex |
|-------|--------------|----------------|
| Surface primary | `#000000` (Black) | `#FFFFFF` (White) |
| Text primary | `#FFFFFF` | `#000000` |
| Accent / interactive | `#4F00B5` (Solidigm Purple) | `#4F00B5` |
| Highlight | `#00FFEC` (Electric Teal) | `#00FFEC` |

---

## Icons

- Use the same SVG source files from `brand/assets/icons/`.
- Render as `Image(systemName:)` only for system icons. Brand icons must use the canonical SVG paths.
- `arrow-double.svg`: use `currentColor` via `foregroundColor` modifier.
- `chevron-down.svg`: always Electric Teal (`#00FFEC`) — do not override.
- Icon sizes: `icon.size.xs` (16pt) → `icon.size.md` (32pt). See `tokens/icons.json`.

---

## Shape / Notch

- The 45° notch can be applied using `Path` + `clipShape` in SwiftUI or `CAShapeLayer` in UIKit.
- Hero / splash screen images should use the notch clip to maintain brand consistency with web.
- Sharp corners (`borderRadius: 0`) are the default — use rounded corners only for interactive affordances (buttons, chips).

---

## Spacing

- Use the same 4px grid from `tokens/space.json`.
- iOS point ≈ CSS pixel at 1× — direct mapping is valid.
- Safe areas: always respect `safeAreaInsets`. Do not place content behind the notch or home indicator.
- Bottom nav padding: add `space.5` (20px) above the home indicator safe area.

---

## Motion

| Token | Value | SwiftUI equivalent |
|-------|-------|--------------------|
| `motion.base` | 300ms | `.easeInOut(duration: 0.3)` |
| `motion.slow` | 500ms | `.easeInOut(duration: 0.5)` |
| `motion.arrowNudge` | 4px translate | `offset(x: 4)` |
| `motion.chevronFlip` | 180° rotate | `.rotationEffect(.degrees(180))` |

- Respect `UIAccessibility.isReduceMotionEnabled` — disable all non-essential animation.
- Accordion disclosure: use `.animation(.easeInOut(duration: 0.5))` on height/opacity.

---

## Accessibility

- VoiceOver: all interactive elements must have `accessibilityLabel`.
- Minimum tap target: 44×44pt (Apple HIG requirement).
- Accordion: use `DisclosureGroup` (SwiftUI) or implement `accessibilityHint` for custom toggles.
- Color alone must never convey state — pair with icon or text.

---

## Do Nots

- Do not use Sequel100 on iOS — it is print-only.
- Do not override system Dynamic Type scaling without accessibility justification.
- Do not hardcode hex values — implement a token-mapped color system.
- Do not render the Electric Teal chevron in a different color for iOS — it is a brand constant.
