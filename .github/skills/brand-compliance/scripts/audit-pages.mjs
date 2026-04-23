#!/usr/bin/env node
/**
 * Brand compliance audit — walks a built site directory, extracts
 * visible text + inline styles + CSS variable references from each
 * HTML page, POSTs to the solidigm-brand MCP server's /api/validate
 * endpoint, and writes a markdown report under docs/brand-audit-<date>.md.
 *
 * Usage:
 *   node .github/skills/brand-compliance/scripts/audit-pages.mjs [siteDir] [--report path]
 *
 * Env:
 *   BRAND_MCP_URL  default http://localhost:8080
 */
import { readFileSync, writeFileSync, mkdirSync, readdirSync, statSync } from 'node:fs';
import { join, relative, resolve, dirname } from 'node:path';

const MCP = (process.env.BRAND_MCP_URL || 'http://localhost:8080').replace(/\/$/, '');

const args = process.argv.slice(2);
let siteDir = 'site/dist';
let reportPath = null;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--report') { reportPath = args[++i]; }
  else if (!args[i].startsWith('-')) { siteDir = args[i]; }
}
const absSiteDir = resolve(siteDir);
const today = new Date().toISOString().slice(0, 10);
if (!reportPath) reportPath = `docs/brand-audit-${today}.md`;

// ---------- helpers ----------
function walk(dir) {
  const out = [];
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    const st = statSync(full);
    if (st.isDirectory()) out.push(...walk(full));
    else if (entry.endsWith('.html')) out.push(full);
  }
  return out;
}

/** Strip <script>/<style>, return visible text + all inline style= values + var(--x) refs. */
function extractAuditable(html) {
  // Remove audit-exempt blocks — legitimate counter-examples, semantic-color
  // swatches, and intentionally-broken demos that should NOT be validated.
  // Authors wrap with: <!-- brand-audit:exempt -->...<!-- /brand-audit:exempt -->
  const noExempt = html.replace(
    /<!--\s*brand-audit:exempt\s*-->[\s\S]*?<!--\s*\/brand-audit:exempt\s*-->/gi,
    ' '
  );
  const noScript = noExempt.replace(/<script[\s\S]*?<\/script>/gi, ' ');
  const noStyleBlock = noScript.replace(/<style[\s\S]*?<\/style>/gi, ' ');

  // inline style attribute contents
  const inlineStyles = [...noStyleBlock.matchAll(/style\s*=\s*"([^"]+)"/gi)]
    .map((m) => m[1])
    .join('; ');

  // headings with case preserved
  const headings = [...noStyleBlock.matchAll(/<h[1-6][^>]*>([\s\S]*?)<\/h[1-6]>/gi)]
    .map((m) => m[1].replace(/<[^>]+>/g, '').trim())
    .filter(Boolean)
    .map((h) => `# ${h}`)
    .join('\n');

  // visible body text
  const text = noStyleBlock
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/\s+/g, ' ')
    .trim();

  return [headings, inlineStyles, text].filter(Boolean).join('\n\n');
}

function grade(errors, warnings) {
  if (errors === 0 && warnings === 0) return 'A+';
  if (errors === 0 && warnings <= 2) return 'A';
  if (errors <= 2) return 'B';
  if (errors <= 5) return 'C';
  return 'F';
}

function pickPlatform(relPath) {
  // Heuristic — all Astro pages here are marketing-flavored. Override if project grows.
  return 'marketing';
}

async function validate(content, platform) {
  const res = await fetch(`${MCP}/api/validate`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ content, platform }),
  });
  if (!res.ok) throw new Error(`validate ${res.status}: ${await res.text()}`);
  return await res.json();
}

// ---------- main ----------
console.log(`Auditing ${absSiteDir} against ${MCP}`);
const files = walk(absSiteDir).sort();
if (files.length === 0) {
  console.error(`No .html files found under ${absSiteDir}. Did you run 'npm run build'?`);
  process.exit(1);
}

const results = [];
for (const file of files) {
  const relPath = relative(process.cwd(), file);
  const html = readFileSync(file, 'utf8');
  const content = extractAuditable(html);
  if (!content || content.length < 20) {
    results.push({ path: relPath, status: 'skip', reason: 'empty/near-empty' });
    continue;
  }
  try {
    const out = await validate(content, pickPlatform(relPath));
    results.push({
      path: relPath,
      status: out.status,
      errors: out.errors || [],
      warnings: out.warnings || [],
      errorCount: out.error_count ?? (out.errors || []).length,
      warningCount: out.warning_count ?? (out.warnings || []).length,
    });
    const g = grade(out.error_count || 0, out.warning_count || 0);
    console.log(`  ${g.padEnd(2)} ${relPath} — ${out.error_count || 0} errors, ${out.warning_count || 0} warnings`);
  } catch (err) {
    results.push({ path: relPath, status: 'error', reason: String(err) });
    console.log(`  !! ${relPath} — ${err.message}`);
  }
}

// ---------- aggregate ----------
const audited = results.filter((r) => r.status === 'pass' || r.status === 'fail');
const totalErrors = audited.reduce((s, r) => s + r.errorCount, 0);
const totalWarnings = audited.reduce((s, r) => s + r.warningCount, 0);
const avgErrors = audited.length ? totalErrors / audited.length : 0;

let siteGrade;
if (avgErrors === 0 && totalWarnings === 0) siteGrade = 'A+';
else if (avgErrors === 0) siteGrade = 'A';
else if (avgErrors <= 2) siteGrade = 'B';
else if (avgErrors <= 5) siteGrade = 'C';
else siteGrade = 'F';

// top violations
const gateTally = {};
for (const r of audited) {
  for (const e of r.errors) gateTally[e.gate_id] = (gateTally[e.gate_id] || 0) + 1;
  for (const w of r.warnings) gateTally[w.gate_id] = (gateTally[w.gate_id] || 0) + 1;
}
const topViolations = Object.entries(gateTally)
  .sort(([, a], [, b]) => b - a)
  .slice(0, 5);

// ---------- report ----------
const rows = results.map((r) => {
  if (r.status === 'skip' || r.status === 'error') {
    return `| ${r.path} | — | ${r.status} | ${r.reason || ''} |`;
  }
  const g = grade(r.errorCount, r.warningCount);
  return `| ${r.path} | ${g} | ${r.errorCount} | ${r.warningCount} |`;
});

const details = audited
  .filter((r) => r.errors.length || r.warnings.length)
  .map((r) => {
    const errorLines = r.errors.map((e) => `  - **ERROR** \`${e.gate_id}\` — ${e.message}`).join('\n');
    const warnLines = r.warnings.map((w) => `  - _WARN_ \`${w.gate_id}\` — ${w.message}`).join('\n');
    return `### ${r.path}\n${errorLines}\n${warnLines}`.trim();
  })
  .join('\n\n');

const report = `# Solidigm Brand Compliance Audit — ${today}

_Generated by the \`brand-compliance\` Skill against \`${absSiteDir}\`._

## Executive summary

- **Site grade:** ${siteGrade}
- **Pages audited:** ${audited.length} of ${results.length}
- **Total errors:** ${totalErrors}
- **Total warnings:** ${totalWarnings}
- **Average errors per page:** ${avgErrors.toFixed(2)}

### Top violations

${
  topViolations.length
    ? topViolations.map(([id, n]) => `- \`${id}\` — ${n} occurrence${n === 1 ? '' : 's'}`).join('\n')
    : '_None — every page passes._'
}

## Per-page results

| Page | Grade | Errors | Warnings |
|------|-------|--------|----------|
${rows.join('\n')}

${details ? '## Detailed findings\n\n' + details : '## Detailed findings\n\n_All audited pages pass._'}

---

_Report-only. This audit does not gate CI. Re-run with:_
\`\`\`bash
node .github/skills/brand-compliance/scripts/audit-pages.mjs ${siteDir}
\`\`\`
`;

mkdirSync(dirname(reportPath), { recursive: true });
writeFileSync(reportPath, report, 'utf8');
console.log(`\nSite grade: ${siteGrade}`);
console.log(`Report written to: ${reportPath}`);
