# Figma incoming exports

Drop Figma → Tokens Studio (or any DTCG-shaped) JSON exports here, then run:

```bash
npm run diff:figma -- figma/incoming/<your-file>.json
# or directly:
node scripts/diff-figma-tokens.mjs figma/incoming/<your-file>.json
```

The script writes a dated report to `docs/figma-snapshot-YYYY-MM-DD.md`
showing drift, Figma-only tokens, and canonical-only tokens.

## Conventions

- Name files `YYYY-MM-DD.json` or `YYYY-MM-DD-<context>.json` (e.g. `2026-04-25-design-system-3.0.json`)
- Files in this folder are **gitignored** — they're working files, not history.
- The dated report under `docs/` is what gets committed.

## Path-prefix caveat

The diff script compares tokens by their dot-path. If your Figma export wraps
everything in a `color.*` / `typography.*` namespace (the default for Tokens
Studio exports — see existing `figma/tokens.json`) but the canonical
`tokens/colors.json` and `tokens/typography.json` are at the root, every token
will appear as both Figma-only and canonical-only.

Two fixes:

1. **Configure Tokens Studio export** to flatten the root namespace before
   exporting (recommended — keeps the canonical files clean).
2. **Pre-flatten the JSON** before running the diff, e.g.
   ```bash
   jq '.color * .typography' figma/incoming/raw.json > figma/incoming/flat.json
   ```

The script intentionally does not auto-flatten because that would mask real
structural differences if someone reorganized one side without coordinating.
