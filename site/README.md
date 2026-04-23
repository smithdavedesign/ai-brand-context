# Solidigm Design System — Landing Site

Astro-based documentation landing page for the Solidigm Design System. Self-consumes the token package and UI toolkit from this repo.

## Structure

- **Brand Foundation** — shared identity, voice, logo, color philosophy
- **NPM Token Package track** — `@solidigm/brand-tokens` (tokens, install, usage)
- **UI Toolkit track** — `ui-toolkit.min.css` (components, utilities)

## Dev

```bash
cd site
npm install
npm run dev     # http://localhost:4321
npm run build   # static output → site/dist
```

## Self-Consumption

The site imports tokens directly from `../tokens/*.json` and the CSS toolkit from `../docs/ui-toolkit.min.css`. Any token change rebuilds the site with updated values.
