# @solidigm/brand-tokens

Solidigm brand design tokens — colors, typography, and ESLint enforcement rules for consistent brand implementation across all projects.

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

```bash
# Regenerate all dist files from source tokens
node build.js
```

Source tokens live in `resources/color.styles.tokens.json` and `resources/text.styles.tokens.json`. All generated files are committed to the repo — consumers install the package directly without needing to run a build step.

## License

UNLICENSED — Solidigm internal use only.
