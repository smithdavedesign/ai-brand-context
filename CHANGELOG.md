# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [1.1.0] — 2026-04-27

### Added
- **Brand Showcase page** (`/showcase`) — full dark inspirational page with 12 sections: hero, mission, values, color palette, typography, brand angle (redesigned), icon library, infrastructure illustrations, stats band, voice & tone, motion principles, CTA
- **Light/dark theme toggle** on the showcase page — CSS custom property swap via `data-theme` attribute, persisted to `localStorage`
- **55 brand SVG icons** extracted from design system handoff to `site/public/assets/icons/`
- **Alpha/tint CSS tokens** — 22 new `--white-*`, `--black-*`, `--purple-tint-*` variables replace all hardcoded `rgba()` calls in `global.css`
- **Showcase entry points** — footer Resources column, homepage dark teaser banner, brand page handoff block
- **Sidebar mobile collapse** — toggle button auto-injected via `BaseLayout.astro` script, electric-teal-styled, `localStorage` persistence
- MCP `README.md` now documents Prompts table, telemetry setup, and SharePoint-optional note

### Changed
- **Nav** — dark `ultra-dark-purple` background (was white + backdrop-blur); logo SVG fills → white; GitHub CTA → `btn--primary` (purple)
- **Footer** — `ultra-dark-purple` background (was `solidigm-purple`); column headings → electric teal
- **Homepage hero** — dark/inspirational full-viewport design; electric teal eyebrow; S mark watermark (inline SVG)
- **Heading font-weight** — `ui-toolkit.min.css` corrected from `bold (700)` → `extralight (200)` per token spec
- **H4/H5/H6** — fixed pixel sizes (32/24/20px) replacing erroneous fluid `clamp()` ranges that were too narrow to be useful
- **Secondary button** — hover changed from dark-purple fill + white text → light-gray fill, text unchanged (matches design spec)
- **Ghost button border** — replaced `color-mix()` (CSS L5) with `rgba()` for broader compatibility
- **Tab components** — TypeSpecimen, usage audience tabs, ComponentPreview all converted from pill shape to underline-tab pattern (sharp corners, purple underline, no white-on-purple)
- **`SectionHeader.astro`** — computed inline styles replaced with `.section-header` / `.section-header--center` CSS classes
- **TokenFlowDiagram** — redesigned as dark branded panel (was white-on-white); electric teal labels, arrowheads, fade-in animation
- **Brand angle section** — redesigned from 3-col awkward layout to 2-panel: large S mark left, rules + tiles right
- All embedded HTML previews audited: hardcoded hex → CSS variables, `font-family:Sora` → `var(--font-family-primary)`, spacing → `var(--space-*)`

### Fixed
- Multiple Astro scoping inheritance bugs on dark backgrounds — resolved by: moving affected rules to `global.css`, using inline `style` attributes, or adding `!important` where the cascade was losing to scoped injection
- Tokens index page: Motion, Elevation, Breakpoints cards were orphaned outside their grid container
- Logo SVG fills on brand page — moved from CSS class (Astro scope couldn't reach `polygon` children) to direct `fill=` attributes
- Phil-chip text color — explicit white on dark chips via `:global()` + inline styles
- `color-on-brand` audit violations in ComponentPreview alert demo and showcase "don't" examples — wrapped in `<!-- brand-audit:exempt -->`

### Removed
- `border-radius: 100px` (pill shape) from badge, TypeSpecimen toggle, audience tabs, ColorSwatchGrid WCAG badge — all replaced with `border-radius: 0` per brand angle rule
- `transform: translateY()` and `box-shadow` from all hover states — brand spec prohibits shadows and bounce

---

## [1.0.0] — 2026-04-23

### Added
- **Design token package** `@solidigm/brand-tokens` — 10 token categories (colors, typography, space, breakpoints, radius, shape, motion, elevation, semantic, icons) in 6 output formats (CSS, SCSS, JS/TS, JSON/W3C DTCG, Tailwind preset, Figma Token Studio)
- **Astro documentation site** — 16 pages: Brand, Tokens (×5), Toolkit (×4), Assets, Patterns, Usage, Governance, Showcase, homepage
- **MCP server** `brand_mcp/` — FastMCP Python server with 14 tools, 8 resources, 4 prompts, telemetry, SharePoint integration, OAuth
- **Brand content** `brand/` — 11 topic markdown files, `colors.json`, `quality-gates.yaml` (16 gates), platform overrides
- **VS Code Copilot integration** — `copilot-instructions.md`, file-scoped instructions, `/brand-check` prompt, brand-compliance Skill
- **CI/CD** — publish workflow, validate workflow, MCP smoke test, asset index freshness check
- **ESLint plugin** — `no-hardcoded-brand-colors` and `no-off-brand-colors` rules
- **Tailwind preset** — token-to-Tailwind config transformer
- **Figma Token Studio JSON** — direct import for Token Studio plugin

### Notes
- Initial site grade: **B** (some pages had inline style violations)
- After audit and fix pass: **A+** across all 16 pages
