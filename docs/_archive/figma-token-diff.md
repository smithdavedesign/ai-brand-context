# Token Diff: Source JSON vs Figma Design System 3.0

**Generated:** 2025-04-22
**Figma file:** [Solidigm Design System 3.0 (New Version)](https://www.figma.com/design/Ei8AT6lR0173XP1v8kY3JJ/Solidigm-Design-System-3.0--New-Version-?node-id=791-1493&m=dev)
**Source files:** `docs/text.styles.tokens.json` (exported from earlier Figma version)

**Action needed:** Confirm which values are authoritative so the npm package can be updated.

---

## Desktop — Value Differences

| Token | Property | Source JSON | Figma 3.0 | Notes |
|-------|----------|------------|------------|-------|
| DT Headline 2 | lineHeight | 110% | 72px | Percentage vs fixed — may be equivalent at 62px font size (62 × 1.1 = 68.2px, not 72px) |
| DT Accordion | fontWeight | 200 (ExtraLight) | 300 (Light) | Weight bump |
| DT Caption | fontSize | 14px | 16px | Size increase |
| DT Caption | fontWeight | 200 (ExtraLight) | 300 (Light) | Weight bump |
| DT Caption | lineHeight | 18px | 22px | Follows size increase |
| DT Disclaimer | fontWeight | 200 (ExtraLight) | 300 (Light) | Weight bump |

## Desktop — Matching ✓

DT Hero, DT H1, DT H3, DT H4, DT H5, DT H6, DT Body, DT Category, DT Button/Button Link, DT Breadcrumb — all match.

---

## Mobile — Value Differences

The mobile scale has been systematically reworked. Nearly every token changed.

| Token | Property | Source JSON | Figma 3.0 | Notes |
|-------|----------|------------|------------|-------|
| MB Hero | fontSize | 52px | 42px | Shifted down |
| MB Hero | lineHeight | 58px | 48px | Shifted down |
| MB H1 | fontSize | 42px | 32px | Shifted down |
| MB H1 | lineHeight | 48px | 38px | Shifted down |
| MB H2 | fontSize | 32px | 28px | Shifted down |
| MB H2 | lineHeight | 38px | 34px | Shifted down |
| MB H3 | — | — | — | Match (24px / 28px) |
| MB H4 | fontSize | 18px | 20px | Shifted up |
| MB H4 | lineHeight | 24px | 26px | Shifted up |
| MB H5 | fontSize | 16px | 18px | Shifted up |
| MB H5 | lineHeight | 20px | 22px | Shifted up |
| MB H6 | fontSize | 14px | 16px | Shifted up |
| MB H6 | lineHeight | 18px | 20px | Shifted up |
| MB Accordion | fontSize | 18px | 20px | Shifted up |
| MB Accordion | fontWeight | 200 (ExtraLight) | 300 (Light) | Weight bump |
| MB Accordion | lineHeight | 22px | 26px | Shifted up |
| MB Body | fontSize | 14px | 16px | Shifted up |
| MB Body | lineHeight | 18px | 20px | Shifted up |
| MB Category | fontSize | 14px | 10px | Major change |
| MB Category | lineHeight | 18% | 14px | Was percentage, now fixed px |
| MB Disclaimer | fontSize | 10px | 12px | Shifted up |
| MB Disclaimer | fontWeight | 200 (ExtraLight) | 300 (Light) | Weight bump |
| MB Disclaimer | lineHeight | 12px | 14px | Shifted up |
| MB Breadcrumb | lineHeight | 16px | 14px | Shifted down |

---

## Naming Differences

| Source JSON | Figma 3.0 | Impact |
|------------|------------|--------|
| DT Body | DT Body Copy | Token rename needed if adopting Figma names |
| DT Button | DT Button Link | Token rename needed if adopting Figma names |
| MB Body 1 | MB Body Copy | Token rename needed if adopting Figma names |

---

## Tokens in Source JSON but NOT in Figma 3.0

| Token | Current Values | Decision Needed |
|-------|---------------|-----------------|
| MB Caption | 16px / 200 / 20px / capitalize | Remove or keep? Not present in Figma 3.0 |

---

## Weight Pattern

Multiple tokens shifted from 200 (ExtraLight) to 300 (Light) in Figma 3.0:
- DT Accordion, DT Caption, DT Disclaimer
- MB Accordion, MB Disclaimer

This looks like an intentional readability improvement across secondary text styles.

---

## Decision Checklist

For each section, mark the authoritative source:

- [ ] **Desktop values** — Use Source JSON / Use Figma 3.0
- [ ] **Mobile values** — Use Source JSON / Use Figma 3.0
- [ ] **Token names** — Keep current names / Adopt Figma 3.0 names (breaking change)
- [ ] **MB Caption** — Keep / Remove
- [ ] **MB Category lineHeight 18%** — Confirm intended value (Figma says 14px)
- [ ] **Weight bumps (200→300)** — Approved change? Apply across the board?

---

*Once decisions are marked, the source tokens will be updated, `node build.js` re-run, and a new version published.*
