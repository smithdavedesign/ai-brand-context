# Platform Overrides: Web — React

Applies to: React SPAs, component libraries, Storybook, internal dashboards.

## Design Tokens
- Import tokens from `@solidigm/brand-context/tokens` or the Tailwind preset
- Use CSS custom properties via the UI toolkit or Tailwind config
- Never hard-code hex values — always reference tokens

## Typography
- Load Sora from Google Fonts via `<link>` or font-face declarations
- Fallback stack: `Sora, -apple-system, BlinkMacSystemFont, sans-serif`
- For CJK content: include Noto Sans alongside Sora

## Color
- Follow the same light/dark mode rules as web-nextjs
- Solidigm Purple as primary interactive color
- Accent colors only for highlights (badges, small indicators)

## Components
- Buttons: Sora SemiBold (600), 10px, uppercase, 2px letter-spacing
- Card backgrounds: White or Light Gray; borders in Gray or Light Gray
- Icon components: single stroke weight, no fills, 16–200px range
- Props should reference token names, not raw values (e.g., `color="solidigm-purple"` not `color="#4f00b5"`)

## Accessibility
- WCAG 2.1 AA contrast (4.5:1) on all text and interactive elements
- Use `aria-label` and semantic HTML
- Keyboard navigation support on all interactive components

## Storybook
- Stories should demonstrate brand-compliant states (light/dark, sizes, variants)
- Include a "Brand Compliance" section in component docs
