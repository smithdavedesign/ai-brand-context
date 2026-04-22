/**
 * @solidigm/brand-tokens ESLint plugin
 *
 * Flat-config compatible. Covers JS, TS, and CSS files.
 *
 * Rules:
 *   no-hardcoded-brand-colors  (warn)  — brand hex used raw instead of token
 *   no-off-brand-colors        (error) — hex color not in brand palette at all
 */
'use strict';

// ---------------------------------------------------------------------------
// Brand palette — canonical hex values (lowercase for comparison)
// ---------------------------------------------------------------------------

const BRAND_COLORS = {
  '#4f00b5': 'solidigm-purple',
  '#8d59cf': 'light-purple',
  '#2f006b': 'dark-purple',
  '#160231': 'ultra-dark-purple',
  '#00083f': 'dark-blue',
  '#21201f': 'dark-grey',
  '#000000': 'black',
  '#ffffff': 'white',
  '#f5f3f1': 'light-gray',
  '#a5a29d': 'gray',
  '#52514f': 'medium-gray',
  '#00ffec': 'electric-teal',
  '#ea11bc': 'electric-pink',
  '#ffa42c': 'orange',
};

const BRAND_HEX_SET = new Set(Object.keys(BRAND_COLORS));

// Short-form aliases that map to palette entries
const SHORT_TO_LONG = {
  '#000': '#000000',
  '#fff': '#ffffff',
};

// Matches 3, 4, 6, or 8 digit hex colors
const HEX_RE = /#(?:[0-9a-f]{8}|[0-9a-f]{6}|[0-9a-f]{3,4})\b/gi;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Normalize a hex string to lowercase 6-digit form when possible. */
function normalizeHex(hex) {
  const lower = hex.toLowerCase();
  if (SHORT_TO_LONG[lower]) return SHORT_TO_LONG[lower];
  // Expand 3-digit shorthand: #abc → #aabbcc
  if (/^#[0-9a-f]{3}$/i.test(lower)) {
    const [, r, g, b] = lower;
    return `#${r}${r}${g}${g}${b}${b}`;
  }
  return lower;
}

/** Extract all hex-color occurrences from a string. */
function findHexColors(str) {
  const results = [];
  let m;
  HEX_RE.lastIndex = 0;
  while ((m = HEX_RE.exec(str)) !== null) {
    results.push({ raw: m[0], normalized: normalizeHex(m[0]), index: m.index });
  }
  return results;
}

// ---------------------------------------------------------------------------
// Rule: no-hardcoded-brand-colors
// ---------------------------------------------------------------------------

const noHardcodedBrandColors = {
  meta: {
    type: 'suggestion',
    docs: {
      description:
        'Warn when a Solidigm brand hex color is hardcoded instead of using the design token variable.',
    },
    schema: [],
    messages: {
      hardcoded:
        "Hardcoded brand color '{{raw}}' — use the token '--solidigm-color-{{token}}' (or the equivalent JS/SCSS variable) instead.",
    },
  },
  create(context) {
    function check(node, value) {
      if (typeof value !== 'string') return;
      for (const { raw, normalized } of findHexColors(value)) {
        if (BRAND_HEX_SET.has(normalized)) {
          context.report({
            node,
            messageId: 'hardcoded',
            data: { raw, token: BRAND_COLORS[normalized] },
          });
        }
      }
    }

    return {
      Literal(node) {
        check(node, node.value);
      },
      TemplateLiteral(node) {
        for (const quasi of node.quasis) {
          check(node, quasi.value.raw);
        }
      },
    };
  },
};

// ---------------------------------------------------------------------------
// Rule: no-off-brand-colors
// ---------------------------------------------------------------------------

const noOffBrandColors = {
  meta: {
    type: 'problem',
    docs: {
      description:
        'Error when a hex color is used that is not part of the Solidigm brand palette.',
    },
    schema: [],
    messages: {
      offBrand:
        "Color '{{raw}}' is not in the Solidigm brand palette. Use an approved brand token instead.",
    },
  },
  create(context) {
    function check(node, value) {
      if (typeof value !== 'string') return;
      for (const { raw, normalized } of findHexColors(value)) {
        // 8-digit hex (with alpha) — skip, these are typically runtime-computed
        if (/^#[0-9a-f]{8}$/i.test(raw)) continue;
        // 4-digit hex (shorthand with alpha) — skip
        if (/^#[0-9a-f]{4}$/i.test(raw)) continue;
        if (!BRAND_HEX_SET.has(normalized)) {
          context.report({
            node,
            messageId: 'offBrand',
            data: { raw },
          });
        }
      }
    }

    return {
      Literal(node) {
        check(node, node.value);
      },
      TemplateLiteral(node) {
        for (const quasi of node.quasis) {
          check(node, quasi.value.raw);
        }
      },
    };
  },
};

// ---------------------------------------------------------------------------
// CSS Processor
// ---------------------------------------------------------------------------

/**
 * Allows the ESLint rules to run on .css files by extracting lines that
 * contain hex colors and wrapping them as synthetic JS string literals.
 */
const cssProcessor = {
  preprocess(text) {
    const lines = text.split('\n');
    const jsLines = [];
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      HEX_RE.lastIndex = 0;
      if (HEX_RE.test(line)) {
        // Escape the line for embedding in a JS string literal
        const escaped = line.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
        jsLines.push({
          text: `'${escaped}';\n`,
          originalLine: i,
        });
      }
    }
    // Return a single code block for ESLint to parse as JS
    const code = jsLines.map((l) => l.text).join('');
    // Store line map in shared state via a closure hack — we attach it to the code string
    cssProcessor._lineMap = jsLines.map((l) => l.originalLine);
    return [code];
  },
  postprocess(messages) {
    const lineMap = cssProcessor._lineMap || [];
    // messages[0] is the array of messages from our single code block
    const mapped = (messages[0] || []).map((msg) => {
      const syntheticLine = (msg.line || 1) - 1; // 0-indexed into our synthetic lines
      const originalLine = lineMap[syntheticLine];
      return {
        ...msg,
        line: originalLine != null ? originalLine + 1 : msg.line,
      };
    });
    return mapped;
  },
  supportsAutofix: false,
};

// ---------------------------------------------------------------------------
// Plugin export (flat config compatible)
// ---------------------------------------------------------------------------

const plugin = {
  meta: {
    name: '@solidigm/brand-tokens',
    version: '1.0.0',
  },
  rules: {
    'no-hardcoded-brand-colors': noHardcodedBrandColors,
    'no-off-brand-colors': noOffBrandColors,
  },
  processors: {
    css: cssProcessor,
  },
};

// Attach configs after plugin object is created (needs self-reference)
plugin.configs = {
  recommended: [
    {
      plugins: {
        '@solidigm/brand-tokens': plugin,
      },
      rules: {
        '@solidigm/brand-tokens/no-hardcoded-brand-colors': 'warn',
        '@solidigm/brand-tokens/no-off-brand-colors': 'error',
      },
    },
    {
      files: ['**/*.css'],
      processor: '@solidigm/brand-tokens/css',
      plugins: {
        '@solidigm/brand-tokens': plugin,
      },
      rules: {
        '@solidigm/brand-tokens/no-hardcoded-brand-colors': 'warn',
        '@solidigm/brand-tokens/no-off-brand-colors': 'error',
      },
    },
  ],
};

module.exports = plugin;
