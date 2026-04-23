# Platform Overrides: Web — Next.js

Applies to: Next.js applications (solidigm.com, partner portals, internal tools).

## Design Tokens
- Import tokens from `@solidigm/brand-context/tokens` or the Tailwind preset
- Use CSS custom properties from the Solidigm UI toolkit where available
- Never hard-code hex values — always reference tokens

## Typography
- Font loading: use `next/font` with Sora (Google Fonts) as primary
- Fallback stack: `Sora, -apple-system, BlinkMacSystemFont, sans-serif`
- For CJK content: load Noto Sans via `next/font` alongside Sora

## Color
- Dark mode: use Ultra Dark Purple or Dark Blue backgrounds with White/Light Gray text
- Light mode: White or Light Gray backgrounds with Dark Gray/Dark Blue text
- Solidigm Purple as primary interactive color (links, buttons, focus rings)

## Components
- Buttons: Sora SemiBold (600), 10px, uppercase, 2px letter-spacing
- Use `tailwind/preset.js` for consistent spacing, colors, and typography scales
- Icon components: render at 16–200px, single stroke weight, no fills

## Accessibility
- All interactive elements must meet WCAG 2.1 AA contrast (4.5:1)
- Focus indicators required on all interactive elements
- Semantic HTML with proper heading hierarchy

## Images
- Use `next/image` with proper `alt` text
- AI-generated images must flagged with `data-ai-generated="true"` attribute
- Never generate logos or brand marks in code — use the provided SVG/PNG assets
