#!/usr/bin/env node
/**
 * build-asset-index.mjs — N2 from the strategic report.
 *
 * Walks the repo and builds `brand/asset-index.json` mapping every
 * brand asset (under `site/public/assets/**`) to the code paths that
 * reference it. Read at startup by `brand_mcp/composer/assets.py` and
 * merged into the asset records returned by `list_assets`.
 *
 * Usage:  node scripts/build-asset-index.mjs
 *
 * Output shape (brand/asset-index.json):
 *   {
 *     "generated_at": "2026-04-24T...",
 *     "asset_count": 87,
 *     "index": {
 *       "logo/Solidigm-logo-purple.svg": [
 *         "site/src/pages/index.astro:42",
 *         "site/src/components/Header.astro:18"
 *       ],
 *       ...
 *     }
 *   }
 */
import { readFile, readdir, stat, writeFile, mkdir } from "node:fs/promises";
import { join, relative, sep } from "node:path";
import { fileURLToPath } from "node:url";

const REPO_ROOT = fileURLToPath(new URL("..", import.meta.url));
const ASSETS_ROOT = join(REPO_ROOT, "site/public/assets");
const SEARCH_ROOTS = [
  "site/src",
  "tailwind",
  "docs",
  "brand",
  ".github",
];
const SEARCH_EXTENSIONS = new Set([
  ".astro",
  ".tsx",
  ".jsx",
  ".ts",
  ".js",
  ".mjs",
  ".css",
  ".scss",
  ".md",
  ".mdx",
  ".html",
  ".vue",
  ".json",
  ".yaml",
  ".yml",
]);
const SKIP_DIRS = new Set(["node_modules", ".git", "dist", ".astro", "_archive"]);

async function* walk(dir) {
  let entries;
  try {
    entries = await readdir(dir, { withFileTypes: true });
  } catch {
    return;
  }
  for (const entry of entries) {
    if (entry.name.startsWith(".") && entry.name !== ".github") continue;
    if (SKIP_DIRS.has(entry.name)) continue;
    const full = join(dir, entry.name);
    if (entry.isDirectory()) {
      yield* walk(full);
    } else if (entry.isFile()) {
      yield full;
    }
  }
}

async function listAssetFilenames() {
  const out = [];
  for await (const file of walk(ASSETS_ROOT)) {
    const rel = relative(ASSETS_ROOT, file).split(sep).join("/");
    out.push({ rel, basename: rel.split("/").pop() });
  }
  return out;
}

async function listSearchFiles() {
  const out = [];
  const indexPath = join(REPO_ROOT, "brand/asset-index.json");
  for (const root of SEARCH_ROOTS) {
    const abs = join(REPO_ROOT, root);
    for await (const file of walk(abs)) {
      // Don't include the index itself — it self-matches every asset.
      if (file === indexPath) continue;
      const ext = "." + file.split(".").pop();
      if (!SEARCH_EXTENSIONS.has(ext)) continue;
      out.push(file);
    }
  }
  return out;
}

async function buildIndex() {
  const assets = await listAssetFilenames();
  const sourceFiles = await listSearchFiles();

  // Pre-build a map of basename → [rel] so a single file scan can match
  // many asset references in O(1) per token.
  const basenameToRel = new Map();
  for (const a of assets) {
    if (!basenameToRel.has(a.basename)) basenameToRel.set(a.basename, []);
    basenameToRel.get(a.basename).push(a.rel);
  }

  const index = {};
  for (const a of assets) index[a.rel] = [];

  for (const file of sourceFiles) {
    let content;
    try {
      content = await readFile(file, "utf-8");
    } catch {
      continue;
    }
    const lines = content.split("\n");
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      // Cheap pre-filter: most asset references contain "/assets/" or end
      // in a known extension. Skip otherwise.
      if (!line.includes("/assets/") && !/\.(svg|png|jpe?g|webp|gif|pdf|eps|ai)\b/i.test(line)) {
        continue;
      }
      for (const [basename, rels] of basenameToRel) {
        if (!line.includes(basename)) continue;
        for (const rel of rels) {
          // If the line mentions either the basename alone OR the full rel
          // path, count it. Prefer rel-path matches when available.
          const hit = line.includes(rel) ? rel : null;
          const fallback = !hit && line.includes(basename) ? rel : null;
          const winner = hit ?? fallback;
          if (!winner) continue;
          const repoRel = relative(REPO_ROOT, file).split(sep).join("/");
          const ref = `${repoRel}:${i + 1}`;
          if (!index[winner].includes(ref)) {
            index[winner].push(ref);
          }
        }
      }
    }
  }

  return {
    generated_at: new Date().toISOString(),
    asset_count: assets.length,
    referenced_count: Object.values(index).filter((v) => v.length > 0).length,
    index,
  };
}

async function main() {
  const result = await buildIndex();
  const outPath = join(REPO_ROOT, "brand/asset-index.json");
  await mkdir(join(REPO_ROOT, "brand"), { recursive: true });
  await writeFile(outPath, JSON.stringify(result, null, 2) + "\n");
  console.log(
    `[build-asset-index] wrote ${outPath} — ` +
      `${result.referenced_count}/${result.asset_count} assets referenced in code`,
  );
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
