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
let fixMode = false;     // --fix      : write patch only (no edits)
let applyMode = false;   // --apply    : write patch AND apply edits
let fixSourceDir = 'site/src';
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--report') { reportPath = args[++i]; }
  else if (args[i] === '--fix') { fixMode = true; }
  else if (args[i] === '--apply') { applyMode = true; fixMode = true; }
  else if (args[i] === '--fix-src') { fixSourceDir = args[++i]; }
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

// ===========================================================================
// Auto-fix pass (N5) — runs when --fix or --apply is set.
// Operates on SOURCE files (default site/src/), not the built HTML.
// ===========================================================================
if (fixMode) {
  console.log(`\nRunning auto-fix pass on ${fixSourceDir}…`);
  const palette = loadPalette();
  const sourceFiles = walkSource(resolve(fixSourceDir));
  const patches = [];   // {file, line, before, after, severity, gate, reason}

  for (const file of sourceFiles) {
    const original = readFileSync(file, 'utf8');
    const lines = original.split('\n');

    let inExempt = false;
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];

      // Respect <!-- brand-audit:exempt --> blocks (same convention as the validator).
      if (/<!--\s*brand-audit:exempt\s*-->/i.test(line)) { inExempt = true; continue; }
      if (/<!--\s*\/brand-audit:exempt\s*-->/i.test(line)) { inExempt = false; continue; }
      if (inExempt) continue;

      // 1. AUTO-FIX: Solidigm® → Solidigm™
      if (/Solidigm®/.test(line)) {
        const fixed = line.replace(/Solidigm®/g, 'Solidigm™');
        patches.push({
          file: relative(process.cwd(), file),
          line: i + 1,
          before: line,
          after: fixed,
          severity: 'auto',
          gate: 'trademark',
          reason: 'Use ™ — Solidigm has no registered ® mark.',
        });
      }

      // 2. SUGGEST: off-palette hex → nearest palette match (only inside style/CSS contexts)
      const hexMatches = [...line.matchAll(/#([0-9a-f]{6}|[0-9a-f]{3})\b/gi)];
      for (const m of hexMatches) {
        const hex = normalizeHex(m[0]);
        if (palette.has(hex)) continue; // already on palette

        // Only fix hexes that look like color values, not ids, fragments, etc.
        // Look for context: style=, color:, background:, fill=, stroke=, --token-name:
        const ctx = line.slice(Math.max(0, m.index - 30), m.index);
        if (!/(color|background|fill|stroke|--[\w-]+|style)\s*[:=]\s*['"]?$/i.test(ctx)) continue;

        const nearest = nearestPaletteColor(hex, palette);
        if (!nearest) continue;
        if (nearest.distance > 60) continue; // too far — don't suggest

        patches.push({
          file: relative(process.cwd(), file),
          line: i + 1,
          before: line,
          after: line.slice(0, m.index) + nearest.hex + line.slice(m.index + m[0].length),
          severity: 'suggest',
          gate: 'palette',
          reason: `${m[0]} → ${nearest.hex} (${nearest.name}, ΔE≈${nearest.distance.toFixed(1)})`,
        });
      }

      // 3. SUGGEST: ALL-CAPS heading → Title Case
      const headingMatch = line.match(/(<h[1-6][^>]*>)([^<]+)(<\/h[1-6]>)/i);
      if (headingMatch) {
        const text = headingMatch[2].trim();
        if (text.length >= 4 && text === text.toUpperCase() && /[A-Z]/.test(text)) {
          const titled = toTitleCase(text);
          if (titled !== text) {
            const fixed = line.replace(headingMatch[0], headingMatch[1] + titled + headingMatch[3]);
            patches.push({
              file: relative(process.cwd(), file),
              line: i + 1,
              before: line,
              after: fixed,
              severity: 'suggest',
              gate: 'headline-case',
              reason: `Headline appears all-caps; suggest Title Case.`,
            });
          }
        }
      }
    }
  }

  if (patches.length === 0) {
    console.log('  No fixable issues found.');
  } else {
    const patchPath = `docs/brand-fixes-${today}.patch`;
    const summaryPath = `docs/brand-fixes-${today}.md`;
    writeUnifiedPatch(patchPath, patches);
    writeFixesSummary(summaryPath, patches);
    console.log(`  Found ${patches.length} fixable findings.`);
    console.log(`  Patch:    ${patchPath}`);
    console.log(`  Summary:  ${summaryPath}`);

    if (applyMode) {
      const auto = patches.filter((p) => p.severity === 'auto');
      applyPatches(auto);
      console.log(`  Applied ${auto.length} auto-fix patches in place.`);
      console.log(`  ${patches.length - auto.length} suggestions left for review (see patch file).`);
    } else {
      console.log(`  Re-run with --apply to write the auto-fixes (suggestions stay in the patch).`);
    }
  }
}

// ===========================================================================
// Fix-mode helpers
// ===========================================================================
function walkSource(dir) {
  const out = [];
  const skip = new Set(['node_modules', 'dist', '.astro', '.git']);
  if (!statSync(dir, { throwIfNoEntry: false })?.isDirectory()) return out;
  for (const entry of readdirSync(dir)) {
    if (skip.has(entry) || entry.startsWith('.')) continue;
    const full = join(dir, entry);
    const st = statSync(full);
    if (st.isDirectory()) out.push(...walkSource(full));
    else if (/\.(astro|tsx|jsx|ts|js|md|mdx|html|vue|css|scss)$/i.test(entry)) out.push(full);
  }
  return out;
}

function normalizeHex(h) {
  let v = h.toLowerCase();
  if (!v.startsWith('#')) v = '#' + v;
  if (v.length === 4) {
    v = '#' + v[1] + v[1] + v[2] + v[2] + v[3] + v[3];
  }
  return v;
}

function loadPalette() {
  const palette = new Map(); // hex → {name, rgb}
  try {
    const raw = JSON.parse(readFileSync(resolve('brand/colors.json'), 'utf8'));
    for (const group of Object.values(raw)) {
      if (!group || typeof group !== 'object') continue;
      for (const [name, def] of Object.entries(group)) {
        if (def && def.hex && Array.isArray(def.rgb)) {
          palette.set(normalizeHex(def.hex), { name, rgb: def.rgb });
        }
      }
    }
  } catch (err) {
    console.warn('  (palette load failed: ' + err.message + ')');
  }
  return palette;
}

function nearestPaletteColor(hex, palette) {
  const target = hexToRgb(hex);
  if (!target) return null;
  let best = null;
  for (const [pHex, def] of palette) {
    const d = colorDistance(target, def.rgb);
    if (!best || d < best.distance) best = { hex: pHex, name: def.name, distance: d };
  }
  return best;
}

function hexToRgb(h) {
  const v = normalizeHex(h);
  const m = /^#([0-9a-f]{6})$/i.exec(v);
  if (!m) return null;
  const n = parseInt(m[1], 16);
  return [(n >> 16) & 0xff, (n >> 8) & 0xff, n & 0xff];
}

function colorDistance(a, b) {
  // Quick perceptual-ish distance (weighted Euclidean — good enough for snap-suggest).
  const dr = a[0] - b[0], dg = a[1] - b[1], db = a[2] - b[2];
  const rMean = (a[0] + b[0]) / 2;
  return Math.sqrt(
    (2 + rMean / 256) * dr * dr +
    4 * dg * dg +
    (2 + (255 - rMean) / 256) * db * db,
  );
}

function toTitleCase(s) {
  const small = new Set(['a','an','and','as','at','but','by','for','if','in','of','on','or','the','to','vs','with']);
  return s.toLowerCase().split(/\s+/).map((w, i) => {
    if (i > 0 && small.has(w)) return w;
    return w.charAt(0).toUpperCase() + w.slice(1);
  }).join(' ');
}

function writeUnifiedPatch(path, patches) {
  // Group patches by file so the patch reads naturally.
  const byFile = new Map();
  for (const p of patches) {
    if (!byFile.has(p.file)) byFile.set(p.file, []);
    byFile.get(p.file).push(p);
  }

  const out = [];
  out.push(`# Solidigm brand auto-fix patch — ${today}`);
  out.push(`# ${patches.length} findings across ${byFile.size} files.`);
  out.push(`# AUTO   = safe to apply (mechanical replacement)`);
  out.push(`# SUGGEST = review before applying (semantic decision)`);
  out.push('#');
  out.push(`# Apply with: node .github/skills/brand-compliance/scripts/audit-pages.mjs --apply`);
  out.push(`# Or hand-review and commit the parts you want.`);
  out.push('');

  for (const [file, items] of byFile) {
    out.push(`--- a/${file}`);
    out.push(`+++ b/${file}`);
    for (const p of items) {
      out.push(`@@ line ${p.line} @@ ${p.severity.toUpperCase()} ${p.gate}: ${p.reason}`);
      out.push(`-${p.before}`);
      out.push(`+${p.after}`);
    }
    out.push('');
  }

  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, out.join('\n'), 'utf8');
}

function writeFixesSummary(path, patches) {
  const auto = patches.filter((p) => p.severity === 'auto');
  const suggest = patches.filter((p) => p.severity === 'suggest');
  const lines = [];
  lines.push(`# Solidigm brand fixes — ${today}`);
  lines.push('');
  lines.push(`- **Auto-fixable:** ${auto.length}`);
  lines.push(`- **Suggested:** ${suggest.length}`);
  lines.push('');
  lines.push('## Auto-fix (safe to apply with `--apply`)');
  lines.push('');
  if (auto.length === 0) lines.push('_None._');
  for (const p of auto) {
    lines.push(`- \`${p.file}:${p.line}\` — **${p.gate}** — ${p.reason}`);
  }
  lines.push('');
  lines.push('## Suggested (review before applying)');
  lines.push('');
  if (suggest.length === 0) lines.push('_None._');
  for (const p of suggest) {
    lines.push(`- \`${p.file}:${p.line}\` — **${p.gate}** — ${p.reason}`);
  }
  lines.push('');
  lines.push('---');
  lines.push('');
  lines.push(`Full patch: \`docs/brand-fixes-${today}.patch\``);
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, lines.join('\n') + '\n', 'utf8');
}

function applyPatches(patches) {
  // Group by file, apply line-by-line replacements top-down (line numbers stable
  // because we replace the whole line, not insert/delete lines).
  const byFile = new Map();
  for (const p of patches) {
    if (!byFile.has(p.file)) byFile.set(p.file, []);
    byFile.get(p.file).push(p);
  }
  for (const [file, items] of byFile) {
    const original = readFileSync(file, 'utf8');
    const lines = original.split('\n');
    for (const p of items) {
      const idx = p.line - 1;
      if (lines[idx] === p.before) {
        lines[idx] = p.after;
      }
    }
    writeFileSync(file, lines.join('\n'), 'utf8');
  }
}
