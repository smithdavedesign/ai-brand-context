# Solidigm Brand Context

One system. Every touchpoint. This repository is the **canonical source of truth** for the Solidigm design system — brand tokens, UI toolkit, brand assets, guidelines, a public documentation site, and an **MCP server** that unifies all of the above for AI agents and internal tools.

See [`docs/architecture.md`](docs/architecture.md) for the full system architecture and flow diagram.

## What's in this repo

| Path | Description |
|------|-------------|
| `brand/` | **Canonical brand content** — topic markdown files, `colors.json`, `quality-gates.yaml`, platform overrides |
| `tokens/` | Source design tokens (W3C DTCG format) |
| `site/` | Astro documentation site |
| `brand_mcp/` | Python FastMCP server — unified backend for agents & site |
| `assets/` | Raw brand-asset dumps (gitignored; organized copy lives under `site/public/assets/`) |
| `tailwind/` | Tailwind CSS preset |
| `eslint/` | ESLint brand enforcement plugin |
| `figma/` | Figma Token Studio JSON |
| `docs/` | Brand guidelines, audit reports, and architecture diagrams |
| `.github/copilot-instructions.md` | Always-on Copilot rules for this repo |
| `.github/instructions/` | Scoped file-instruction rules (applied via `applyTo` globs) |
| `.github/prompts/` | Reusable Copilot prompts (e.g. `/brand-check`) |
| `.github/skills/` | Multi-step Copilot Skills (e.g. `brand-compliance` site audit) |
| `.vscode/mcp.json` | VS Code Copilot MCP server registration |

---

## MCP Server (`brand_mcp/`)

The Solidigm Brand MCP server exposes the entire design system to AI agents (Claude, Cursor, VS Code Copilot, ChatGPT with MCP support, etc.) and is consumed by the Astro site's `/assets` page.

### Quickstart

```bash
cd brand_mcp
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# …fill in M365_* and BRAND_SHAREPOINT_* values in .env…
python -m brand_mcp.server
# → http://localhost:8080
```

### Use it

- **VS Code Copilot** — `.vscode/mcp.json` is already wired up; pick either the HTTP or stdio server entry.
- **Claude Desktop / Cursor** — add the HTTP URL to your client's MCP config (see [`brand_mcp/README.md`](brand_mcp/README.md)).
- **Astro site** — the `/assets` page calls the MCP server's `/api/assets` endpoint at runtime.

### What it exposes (10 tools)

| Tool | Purpose |
|------|---------|
| `get_design_tokens` | Full W3C DTCG tokens (colors + typography) |
| `get_color` | Fuzzy-match a named color (`solidigm-purple`, `Electric Teal`, etc.) |
| `get_brand_guidelines` | Narrative guidance by topic (voice, logo, typography…) |
| `get_ui_toolkit_class` | Look up a `tk-*` CSS utility class |
| `list_assets` | Unified manifest of local + SharePoint brand assets |
| `get_logo` | Resolve a specific logo variant/color/format |
| `search_brand_source_documents` | Search the SharePoint brand library (when configured) |
| `get_brand_context` | Task/platform-scoped brand context (for AI prompt assembly) |
| `get_brand_system_prompt` | Drop-in system prompt for brand-aware LLM calls |
| `validate_brand_output` | Pass/fail AI-generated content against 16 quality gates |

**Resources:** `brand://tokens/colors`, `brand://tokens/typography`, `brand://guidelines/main`, `brand://toolkit/css`, `brand://assets/manifest`.

**HTTP routes:** `/api/assets` (Astro site), `/api/validate` (brand-compliance Skill), `/api/health`.

Full details in [`brand_mcp/README.md`](brand_mcp/README.md).

---

## VS Code Copilot Skill Layer

Copilot is pre-configured in this repo to enforce brand rules and call the MCP server automatically.

| Primitive | File | What it does |
|-----------|------|--------------|
| Workspace instructions | [`.github/copilot-instructions.md`](.github/copilot-instructions.md) | Always-on: "call `solidigm-brand` tools first; never hallucinate hex/fonts/trademarks" |
| File instructions | [`.github/instructions/solidigm-brand.instructions.md`](.github/instructions/solidigm-brand.instructions.md) | Enforced rules on `.astro/.tsx/.css/.md` files — palette, typography, trademark, do-nots |
| Prompt | [`.github/prompts/brand-check.prompt.md`](.github/prompts/brand-check.prompt.md) | `/brand-check <target>` — validates any file/URL/snippet |
| Skill | [`.github/skills/brand-compliance/SKILL.md`](.github/skills/brand-compliance/SKILL.md) | Full multi-page audit of the built Astro site, emits `docs/brand-audit-<date>.md` |

### Run the site audit

```bash
# 1. Start the MCP server (if not already running)
cd brand_mcp && source .venv/bin/activate && python -m brand_mcp.server &

# 2. Build the site
cd site && npm run build && cd ..

# 3. Run the audit
node .github/skills/brand-compliance/scripts/audit-pages.mjs site/dist
# → docs/brand-audit-YYYY-MM-DD.md
```

The Skill is report-only; it does not gate CI.

---

## Documentation Site (`site/`)

A self-consuming static site that documents the entire design system. It imports tokens and the UI toolkit directly from this repo (dogfooding).

### Run locally

```bash
cd site
npm install
npm run dev
# → http://localhost:4321
```

### Build

```bash
cd site
npm run build
# Output → site/dist/
```

### Pages

| Route | Description |
|-------|-------------|
| `/` | Homepage — system overview and dual-track CTAs |
| `/brand` | Brand foundation — voice, color philosophy, logo rules |
| `/tokens` | Token overview and category index |
| `/tokens/colors` | Live color swatches with WCAG badges |
| `/tokens/typography` | Interactive type specimen (Desktop/Mobile) |
| `/tokens/spacing` | Spacing scale and grid specs |
| `/tokens/usage` | Install and integration guide |
| `/toolkit` | UI toolkit overview |
| `/toolkit/foundations` | Typography, color, and spacing utilities |
| `/toolkit/components` | Atomic design component library |
| `/toolkit/utilities` | Searchable utility class reference |
| `/assets` | Browsable brand asset library (powered by MCP server) |
| `/patterns` | Layout patterns and UX best practices |
| `/usage` | Audience-tabbed guide (Designers/Engineers/Business) |
| `/governance` | Contribution, versioning, and ownership |
| `/showcase` | Before/after proof the site eats its own dog food |

### Brand Assets

Organized under `site/public/assets/` and served at `/assets/`:

```
assets/
  logo/
    s-mark/       {black, purple, blue, white}
    standard/     {black, purple, blue, white}  ← includes SVG
    stacked/      {black, purple, blue, white}
    wordmark/     {black, blue, white}
  illustrations/  19 component illustration PNGs
  docs/           Brand guidelines PDF, trademark PDF, PPT icons
```

---

## NPM Token Package (`@solidigm/brand-tokens`)

## Setup

### 1. Authenticate with GitHub Packages (one-time per machine)

Create or edit `~/.npmrc` and add:

```
//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}
```

Set `GITHUB_TOKEN` as an environment variable containing a GitHub PAT with `read:packages` scope.

### 2. Project `.npmrc`

Add to your project root `.npmrc`:

```
@solidigm:registry=https://npm.pkg.github.com
```

### 3. Install

```bash
npm install @solidigm/brand-tokens
```

---

## Usage

### CSS Custom Properties

```css
/* Import all tokens */
@import '@solidigm/brand-tokens/css';

/* Or import individually */
@import '@solidigm/brand-tokens/css/colors';
@import '@solidigm/brand-tokens/css/typography';

/* Use in your styles */
.hero {
  color: var(--solidigm-color-solidigm-purple);
  font-size: var(--solidigm-type-dt-hero-font-size);
  font-weight: var(--solidigm-type-dt-hero-font-weight);
  line-height: var(--solidigm-type-dt-hero-line-height);
}
```

### SCSS

```scss
@use '@solidigm/brand-tokens/scss' as brand;

// Individual variables
.card {
  background: brand.$solidigm-color-dark-blue;
  font-size: brand.$solidigm-type-dt-body-font-size;
}

// Use the color map
@each $name, $value in brand.$solidigm-colors {
  .bg-#{$name} {
    background-color: $value;
  }
}
```

### JavaScript / TypeScript

```js
// ESM
import { colors, typography } from '@solidigm/brand-tokens';

console.log(colors.solidigmPurple); // '#4f00b5'
console.log(typography.desktop.dtHero.fontSize); // '112px'

// CJS
const { colors, typography } = require('@solidigm/brand-tokens');
```

Full TypeScript types are included — all values are `readonly` with literal types.

### Tailwind CSS

```js
// tailwind.config.js
module.exports = {
  presets: [require('@solidigm/brand-tokens/tailwind')],
  // ...
};
```

Then use in your templates:

```html
<h1 class="text-solidigm-purple text-dt-hero font-sora">Hello</h1>
<p class="text-electric-teal text-dt-body">World</p>
```

### Figma / Token Studio

Import `figma/tokens.json` directly into the [Token Studio](https://tokens.studio) plugin. The file contains `color` and `typography` groups with preserved subgroup structure (Dark/Light/Accents, Desktop/Mobile).

### ESLint

The plugin works with ESLint flat config and covers JS, TS, and CSS files:

```js
// eslint.config.js
import brandTokens from '@solidigm/brand-tokens/eslint';

export default [
  // Spread the recommended config — enables both rules + CSS processor
  ...brandTokens.configs.recommended,

  // ... your other config
];
```

**Rules:**

| Rule | Severity | Description |
|------|----------|-------------|
| `no-hardcoded-brand-colors` | warn | Brand hex code used directly instead of a token variable |
| `no-off-brand-colors` | error | Hex color is not in the Solidigm palette at all |

---

## Token Reference

### Colors

| Token | Hex | CSS Variable | JS Key |
|-------|-----|-------------|--------|
| Solidigm Purple | `#4f00b5` | `--solidigm-color-solidigm-purple` | `solidigmPurple` |
| Light Purple | `#8d59cf` | `--solidigm-color-light-purple` | `lightPurple` |
| Dark Purple | `#2f006b` | `--solidigm-color-dark-purple` | `darkPurple` |
| Ultra Dark Purple | `#160231` | `--solidigm-color-ultra-dark-purple` | `ultraDarkPurple` |
| Dark Blue | `#00083f` | `--solidigm-color-dark-blue` | `darkBlue` |
| Dark Grey | `#21201f` | `--solidigm-color-dark-grey` | `darkGrey` |
| Black | `#000000` | `--solidigm-color-black` | `black` |
| White | `#ffffff` | `--solidigm-color-white` | `white` |
| Light Gray | `#f5f3f1` | `--solidigm-color-light-gray` | `lightGray` |
| Gray | `#a5a29d` | `--solidigm-color-gray` | `gray` |
| Medium Gray | `#52514f` | `--solidigm-color-medium-gray` | `mediumGray` |
| Electric Teal | `#00ffec` | `--solidigm-color-electric-teal` | `electricTeal` |
| Electric Pink | `#ea11bc` | `--solidigm-color-electric-pink` | `electricPink` |
| Orange | `#ffa42c` | `--solidigm-color-orange` | `orange` |

### Typography — Desktop

| Token | Font Size | Weight | Line Height | Letter Spacing | Text Transform |
|-------|-----------|--------|-------------|----------------|----------------|
| DT Hero | 112px | 200 | 110% | 0px | capitalize |
| DT Headline 1 | 72px | 200 | 82px | 0px | capitalize |
| DT Headline 2 | 62px | 200 | 110% | 0px | none |
| DT Headline 3 | 42px | 200 | 48px | 0px | none |
| DT Headline 4 | 32px | 200 | 38px | 0px | none |
| DT Headline 5 | 24px | 200 | 28px | 0px | none |
| DT Headline 6 | 20px | 200 | 26px | 0px | none |
| DT Accordion | 32px | 200 | 38px | 0px | none |
| DT Body | 16px | 200 | 20px | 0px | none |
| DT Caption | 14px | 200 | 18px | 0px | none |
| DT Category | 10px | 600 | 14px | 2px | uppercase |
| DT Button | 10px | 600 | 14px | 2px | uppercase |
| DT Disclaimer | 12px | 200 | 14px | 0px | none |
| DT Breadcrumb | 10px | 700 | 14px | 2px | uppercase |

### Typography — Mobile

| Token | Font Size | Weight | Line Height | Letter Spacing | Text Transform |
|-------|-----------|--------|-------------|----------------|----------------|
| MB Hero | 52px | 200 | 58px | 0px | none |
| MB Headline 1 | 42px | 200 | 48px | 0px | none |
| MB Headline 2 | 32px | 200 | 38px | 0px | none |
| MB Headline 3 | 24px | 200 | 28px | 0px | none |
| MB Headline 4 | 18px | 200 | 24px | 0px | none |
| MB Headline 5 | 16px | 200 | 20px | 0px | none |
| MB Headline 6 | 14px | 200 | 18px | 0px | none |
| MB Accordion | 18px | 200 | 22px | 0px | none |
| MB Body 1 | 14px | 200 | 18px | 0px | none |
| MB Caption | 16px | 200 | 20px | 0px | capitalize |
| MB Category | 14px | 600 | 18% | 2px | uppercase |
| MB Button Link | 10px | 600 | 14px | 2px | uppercase |
| MB Disclaimer | 10px | 200 | 12px | 0px | none |
| MB Breadcrumb | 10px | 700 | 16px | 2px | uppercase |

All typography tokens use **Sora** as the font family.

---

## Exports Map

| Import Path | Format | Description |
|------------|--------|-------------|
| `@solidigm/brand-tokens` | JS (ESM/CJS) | `{ colors, typography }` objects |
| `@solidigm/brand-tokens/css` | CSS | All custom properties |
| `@solidigm/brand-tokens/css/colors` | CSS | Color custom properties only |
| `@solidigm/brand-tokens/css/typography` | CSS | Typography custom properties only |
| `@solidigm/brand-tokens/scss` | SCSS | All variables + maps |
| `@solidigm/brand-tokens/scss/colors` | SCSS | Color variables + map |
| `@solidigm/brand-tokens/scss/typography` | SCSS | Typography variables + map |
| `@solidigm/brand-tokens/tokens` | JSON | Combined W3C DTCG tokens |
| `@solidigm/brand-tokens/tokens/colors` | JSON | Color tokens (DTCG) |
| `@solidigm/brand-tokens/tokens/typography` | JSON | Typography tokens (DTCG) |
| `@solidigm/brand-tokens/tailwind` | JS | Tailwind CSS preset |
| `@solidigm/brand-tokens/figma` | JSON | Figma Token Studio format |
| `@solidigm/brand-tokens/eslint` | JS | ESLint plugin with brand rules |

---

## Development

### Token package

```bash
# Regenerate all dist files from source tokens
node build.js
```

Source tokens live in `tokens/colors.json` and `tokens/typography.json`. All generated files are committed — consumers install the package directly without running a build step.

### Documentation site

```bash
cd site
npm run dev      # local dev server → http://localhost:4321
npm run build    # static build → site/dist/
```

The prebuild script (`site/scripts/sync-toolkit.mjs`) automatically copies `docs/ui-toolkit.min.css` into `site/public/` before each build. All `npm` commands for the site must be run from the `site/` directory.

## License

UNLICENSED — Solidigm internal use only.
