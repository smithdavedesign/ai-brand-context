# Token Expansion Strategy

> Based on the Figma variable audit of 2025-04-25 and the UI Toolkit page
> in **Solidigm Dotcom 3.0 — Dayani** (`BioUSVD6t51ZNeG0g9AcNz`).

---

## Current state

All token categories are now implemented (Phase 10, April 2025).

| Token category | File | Count | Status |
|---------------|------|-------|--------|
| Colors | `tokens/colors.json` | 14 | ✅ Complete |
| Typography | `tokens/typography.json` | 28 | ✅ Complete |
| Space | `tokens/space.json` | 18 | ✅ Implemented |
| Breakpoints | `tokens/breakpoints.json` | 8 | ✅ Implemented |
| Radius | `tokens/radius.json` | 6 | ✅ Implemented |
| Shape | `tokens/shape.json` | — | ✅ Implemented |
| Motion | `tokens/motion.json` | 13 | ✅ Implemented |
| Elevation | `tokens/elevation.json` | 6 | ✅ Implemented |
| Semantic | `tokens/semantic.json` | — | ✅ Implemented |
| Icons | `tokens/icons.json` | — | ✅ Implemented |

All categories are wired into:
- `build.js` (`readSourceTokens()` + `generateUIToolkit()`)
- `brand_mcp/tools/brand.py` (`get_design_tokens` + dedicated tools)
- `tokens/index.json` (unified DTCG bundle)

The values in `tokens/space.json` were validated against the Storybook + AEM
SCSS audit (see `docs/storybook-scss-audit.md`). `tokens/breakpoints.json`
modernizes legacy Bootstrap defaults (576→640, 992→1024) per audit evidence.

---

## Priority 1 — Spacing tokens

**Source:** Section 01 (DT + MB Grid) + Button/Link padding + Form Field layout.

**Proposed file:** `tokens/spacing.json`

```jsonc
{
  "Spacing": {
    "$type": "dimension",
    // Extract from Figma grid section:
    "2xs":  { "$value": "4px" },
    "xs":   { "$value": "8px" },
    "sm":   { "$value": "12px" },
    "md":   { "$value": "16px" },
    "lg":   { "$value": "24px" },
    "xl":   { "$value": "32px" },
    "2xl":  { "$value": "48px" },
    "3xl":  { "$value": "64px" },
    "4xl":  { "$value": "96px" }
  }
}
```

**Action required:** Inspect the DT + MB Grid section (`15967:1991`) with
`get_design_context` to read exact gutter, margin, and padding values. The
values above are placeholders based on common 8px-grid systems — they must be
validated against the Figma comp before committing.

---

## Priority 2 — Border radius tokens

**Source:** Sections 05 (Buttons + Links) and 09 (Interactivity / Cards).

**Proposed file:** `tokens/radii.json`

```jsonc
{
  "Radius": {
    "$type": "dimension",
    "none": { "$value": "0px" },
    "sm":   { "$value": "4px" },
    "md":   { "$value": "8px" },
    "lg":   { "$value": "16px" },
    "full": { "$value": "9999px" }
  }
}
```

**Action required:** Inspect button and card components in Figma to extract
actual corner-radius values. The toolkit uses 45° blade cuts (section 09) which
may indicate `clip-path` usage rather than `border-radius` in some contexts.

---

## Priority 3 — Breakpoint tokens

**Source:** Section 01 (DT + MB Grid).

**Proposed file:** `tokens/breakpoints.json`

```jsonc
{
  "Breakpoints": {
    "$type": "dimension",
    "mobile":  { "$value": "375px" },
    "tablet":  { "$value": "768px" },
    "desktop": { "$value": "1024px" },
    "wide":    { "$value": "1440px" }
  }
}
```

**Action required:** Confirm against artboard widths in the Grid section.
The toolkit visually shows "DT" (desktop) and "MB" (mobile) layouts with
specific column counts.

---

## Priority 4 — Shadow / elevation tokens

**Source:** Not currently specified in Figma.

**Status:** Deferred until the design team adds elevation guidance. The
UI Toolkit page has no shadow/elevation section. If shadows are used in
Storybook components, extract them from the component library instead.

---

## Priority 5 — Component-level tokens

Some UI Toolkit sections describe component *behavior* rather than atomic
design tokens:

| Section | Content type | Token candidate? |
|---------|-------------|-----------------|
| 05 Buttons + Links | Padding, border, hover colors | Yes — extract as component tokens |
| 06 Form Fields | Heights, border, focus ring, error colors | Yes — but complex (stateful) |
| 07 Photo Styling | Crop ratios, overlay specs | No — art direction, not tokens |
| 08 Iconography | Icon sizes, social icon set | Partial — sizing could be tokens |
| 09 Interactivity | Card hover, nav patterns, 45° blades | No — behavioral, not tokens |
| 10 Photography | Photo guidelines | No — editorial |

Component tokens are lower priority than spacing/radius/breakpoints because:
1. They have narrower reuse (one component vs. whole system)
2. They're better managed in Storybook once the Storybook repo is available
3. They change more frequently than foundation tokens

---

## Implementation plan

### Phase A — Foundation tokens (this repo, next session)

1. **Inspect Figma comps** via MCP `get_design_context` on specific nodes
   to extract exact spacing, radius, and breakpoint values.
2. Create `tokens/spacing.json`, `tokens/radii.json`, `tokens/breakpoints.json`
   in W3C DTCG format.
3. Update `build.js` to read and merge the new token files.
4. Update `generateUIToolkit()` to emit CSS custom properties for the new tokens.
5. Run `npm run build` + `npm test` to verify.

### Phase B — Figma library alignment (requires Figma editor access)

1. Publish the 26 missing text styles in the DS 3.0 Figma library.
2. Add the 8 missing colors as Figma variables in the Primitives collection.
3. Create a new "Spacing" variable collection with the extracted values.
4. Create a "Radius" variable collection.

This requires collaboration with the design team or Figma admin access.

### Phase C — Storybook bridge (blocked: needs Storybook repo)

1. Map Storybook atoms/molecules to token categories.
2. Create a pipeline: `Figma → tokens/ → build.js → npm → Storybook`.
3. Component-level tokens (button padding, form heights, etc.) live in
   Storybook's design system, referencing foundation tokens from this package.
4. Storybook consumes `@solidigm/brand-tokens` as a dependency.

### Phase D — Automated drift detection (CI)

1. Script that calls Figma MCP `search_design_system` + reads `tokens/` and
   diffs variable values vs. canonical hex values.
2. Run on a schedule (weekly) or on PR to `tokens/`.
3. Fail CI if any canonical token drifts from the Figma variable value.

---

## Not tokenizing

These decisions are intentional, not oversights:

- **Photography art direction** (section 10) — editorial, not design tokens
- **Iconography assets** (section 08) — managed as assets, not tokens
- **45° blade angles** (section 09) — CSS `clip-path` patterns, not tokens
- **Background application rules** (section 04) — semantic guidance, not values
- **Shadows** — until the design team specifies elevation levels
