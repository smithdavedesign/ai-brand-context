---
description: "Check a file, URL, or pasted content against Solidigm brand quality gates. Returns pass/fail with specific errors and suggested fixes."
argument-hint: "File path, URL, or content to check"
agent: "agent"
tools: ["solidigm-brand/*", "codebase", "editFiles"]
---

# Brand Compliance Check

Check the target for Solidigm brand violations:

**Target:** ${input:target:What should I check? (file path, URL, or paste content)}

## Steps

1. **Resolve the target:**
   - If it's a workspace file path, read it with the codebase tool.
   - If it's a URL, fetch it.
   - If it's pasted content, use it directly.

2. **Call `validate_brand_output`** with the content. If the target is a specific platform (e.g. a `.astro` file → `web-nextjs` or marketing), pass the `platform` argument.

3. **If validation fails**, for each error:
   - Show the offending snippet with line context.
   - Explain the rule (cite the gate ID from `brand/quality-gates.yaml`).
   - Propose a concrete fix using the approved palette/typography.
   - Where helpful, call `get_color` to suggest the nearest approved color by name.

4. **Return a summary** with:
   - Overall status (PASS / FAIL)
   - Error count and warning count
   - Top 3 issues to fix first
   - One-line compliance grade (A+ / A / B / C / F) based on error count:
     - 0 errors, 0 warnings → A+
     - 0 errors, 1–2 warnings → A
     - 1–2 errors → B
     - 3–5 errors → C
     - 6+ errors → F

## Rules

- Do **not** fabricate fixes that are not in `brand/colors.json` or the approved typefaces.
- Always cite the gate ID so the author can look up the rule.
- If the content is too large to validate in one call, split by section/heading and validate each.
