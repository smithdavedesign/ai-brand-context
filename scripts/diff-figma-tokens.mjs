#!/usr/bin/env node
/**
 * diff-figma-tokens.mjs — Phase 10 / Figma route (a)
 *
 * Compares an incoming Figma token export (typically from the Tokens Studio
 * plugin) against the canonical tokens in `tokens/colors.json` and
 * `tokens/typography.json`. Emits a dated markdown report at
 * `docs/figma-snapshot-YYYY-MM-DD.md` with three buckets:
 *
 *   - DRIFT     — same path exists in both, value differs (action required)
 *   - FIGMA-ONLY — path in Figma export but not in canonical tokens
 *   - REPO-ONLY — path in canonical tokens but not in Figma export
 *
 * Usage:
 *   node scripts/diff-figma-tokens.mjs figma/incoming/<file>.json
 *
 * Drop a Figma → Tokens Studio export into `figma/incoming/` and run.
 * Both DTCG ($type/$value) and Tokens Studio (type/value) shapes are
 * handled transparently.
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { resolve, basename, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const REPO_ROOT = fileURLToPath(new URL("..", import.meta.url));
const TODAY = new Date().toISOString().slice(0, 10);

function usage() {
  console.error("Usage: node scripts/diff-figma-tokens.mjs <path-to-incoming.json>");
  console.error("");
  console.error("Drop a Figma export into figma/incoming/ first. Example:");
  console.error("  node scripts/diff-figma-tokens.mjs figma/incoming/2026-04-25.json");
  process.exit(2);
}

const incomingArg = process.argv[2];
if (!incomingArg) usage();
const incomingPath = resolve(incomingArg);
if (!existsSync(incomingPath)) {
  console.error(`File not found: ${incomingPath}`);
  process.exit(2);
}

/** Walk a token tree, yielding {path, type, value} for every leaf. */
function* walkTokens(obj, prefix = []) {
  if (obj === null || typeof obj !== "object") return;

  // Detect a leaf token. Two supported shapes:
  //   DTCG:          { "$type": "color", "$value": "#fff" }
  //   Tokens Studio: { "type":  "color", "value":  "#fff" }
  const dtcgValue = obj["$value"];
  const tsValue = obj["value"];
  const dtcgType = obj["$type"];
  const tsType = obj["type"];

  const hasDtcg = dtcgValue !== undefined;
  const hasTs = tsValue !== undefined && (tsType === undefined || typeof tsType === "string");

  if (hasDtcg || hasTs) {
    yield {
      path: prefix.join("."),
      type: dtcgType ?? tsType ?? "unknown",
      value: hasDtcg ? dtcgValue : tsValue,
    };
    return;
  }

  for (const [key, val] of Object.entries(obj)) {
    if (key.startsWith("$")) continue; // metadata
    yield* walkTokens(val, [...prefix, key]);
  }
}

function loadTokenFile(path) {
  const raw = JSON.parse(readFileSync(path, "utf-8"));
  const map = new Map();
  for (const tok of walkTokens(raw)) {
    map.set(tok.path, tok);
  }
  return map;
}

/** Normalize values for comparison — colors are case-insensitive, etc. */
function normalize(type, value) {
  if (typeof value !== "string") return JSON.stringify(value);
  if (type === "color") {
    let v = value.trim().toLowerCase();
    // expand #abc → #aabbcc
    if (/^#[0-9a-f]{3}$/.test(v)) {
      v = "#" + v[1] + v[1] + v[2] + v[2] + v[3] + v[3];
    }
    return v;
  }
  return value.trim();
}

const incoming = loadTokenFile(incomingPath);

const canonicalFiles = [
  ["colors", resolve(REPO_ROOT, "tokens/colors.json")],
  ["typography", resolve(REPO_ROOT, "tokens/typography.json")],
];

// Merge both canonical files into one map; tag each entry with its source file.
const canonical = new Map();
const canonicalSources = new Map();
for (const [label, path] of canonicalFiles) {
  if (!existsSync(path)) continue;
  for (const tok of walkTokens(JSON.parse(readFileSync(path, "utf-8")))) {
    canonical.set(tok.path, tok);
    canonicalSources.set(tok.path, label);
  }
}

const drift = [];      // { path, type, repoValue, figmaValue, source }
const figmaOnly = [];  // { path, type, value }
const repoOnly = [];   // { path, type, value, source }

for (const [path, fig] of incoming) {
  if (canonical.has(path)) {
    const can = canonical.get(path);
    if (normalize(fig.type, fig.value) !== normalize(can.type, can.value)) {
      drift.push({
        path,
        type: fig.type,
        repoValue: can.value,
        figmaValue: fig.value,
        source: canonicalSources.get(path) ?? "?",
      });
    }
  } else {
    figmaOnly.push({ path, type: fig.type, value: fig.value });
  }
}
for (const [path, can] of canonical) {
  if (!incoming.has(path)) {
    repoOnly.push({
      path,
      type: can.type,
      value: can.value,
      source: canonicalSources.get(path) ?? "?",
    });
  }
}

// ---------- report ----------
const lines = [];
lines.push(`# Figma token snapshot — ${TODAY}`);
lines.push("");
lines.push(`_Source: \`${incomingArg}\` → diffed against \`tokens/{colors,typography}.json\`._`);
lines.push("");
lines.push("## Summary");
lines.push("");
lines.push(`- **Tokens in Figma export:** ${incoming.size}`);
lines.push(`- **Tokens in canonical (\`tokens/\`):** ${canonical.size}`);
lines.push(`- **Drift (same path, different value):** ${drift.length}`);
lines.push(`- **Figma-only (missing from canonical):** ${figmaOnly.length}`);
lines.push(`- **Canonical-only (missing from Figma):** ${repoOnly.length}`);
lines.push("");

if (drift.length) {
  lines.push("## Drift — these need reconciliation");
  lines.push("");
  lines.push("| Path | Type | Repo value | Figma value | Source file |");
  lines.push("|------|------|------------|-------------|-------------|");
  for (const d of drift) {
    lines.push(`| \`${d.path}\` | ${d.type} | \`${d.repoValue}\` | \`${d.figmaValue}\` | \`tokens/${d.source}.json\` |`);
  }
  lines.push("");
  lines.push("> **Action:** decide per row whether the repo or Figma is correct. The repo is the canonical source of truth — if Figma should win, update `tokens/` _and_ open a PR against the design system Figma file noting the change.");
  lines.push("");
} else {
  lines.push("## Drift");
  lines.push("");
  lines.push("_No drift — every overlapping token matches._");
  lines.push("");
}

if (figmaOnly.length) {
  lines.push("## Figma-only — new tokens proposed by design");
  lines.push("");
  lines.push("| Path | Type | Value |");
  lines.push("|------|------|-------|");
  for (const f of figmaOnly.slice(0, 200)) {
    lines.push(`| \`${f.path}\` | ${f.type} | \`${typeof f.value === "string" ? f.value : JSON.stringify(f.value)}\` |`);
  }
  if (figmaOnly.length > 200) lines.push(`| _…and ${figmaOnly.length - 200} more_ | | |`);
  lines.push("");
  lines.push("> **Action:** if these should be canonical, add them to `tokens/colors.json` or `tokens/typography.json`, then `npm run build` to regenerate the published package.");
  lines.push("");
}

if (repoOnly.length) {
  lines.push("## Canonical-only — Figma may be missing them");
  lines.push("");
  lines.push("| Path | Type | Value | Source file |");
  lines.push("|------|------|-------|-------------|");
  for (const r of repoOnly.slice(0, 200)) {
    lines.push(`| \`${r.path}\` | ${r.type} | \`${typeof r.value === "string" ? r.value : JSON.stringify(r.value)}\` | \`tokens/${r.source}.json\` |`);
  }
  if (repoOnly.length > 200) lines.push(`| _…and ${repoOnly.length - 200} more_ | | | |`);
  lines.push("");
  lines.push("> **Action:** review with the design team. Either add to Figma so the export covers them, or remove from `tokens/` if the canonical entry is stale.");
  lines.push("");
}

lines.push("---");
lines.push("");
lines.push(`Generated by \`scripts/diff-figma-tokens.mjs\`. Source file: \`${incomingArg}\`.`);

const reportPath = resolve(REPO_ROOT, `docs/figma-snapshot-${TODAY}.md`);
mkdirSync(dirname(reportPath), { recursive: true });
writeFileSync(reportPath, lines.join("\n") + "\n", "utf-8");

console.log(`[diff-figma-tokens] Compared ${incoming.size} Figma tokens vs ${canonical.size} canonical tokens.`);
console.log(`  Drift:         ${drift.length}`);
console.log(`  Figma-only:    ${figmaOnly.length}`);
console.log(`  Canonical-only: ${repoOnly.length}`);
console.log(`Report: ${reportPath}`);
