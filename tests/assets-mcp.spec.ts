/**
 * Playwright tests for the Solidigm Brand MCP /api/assets endpoint and
 * the assets page filter UX.
 *
 * Run:  cd <repo-root> && npx playwright test
 *
 * Requirements:
 *  - MCP server running on http://localhost:8080  (brand_mcp)
 *  - Astro dev/preview server on http://localhost:4321  (site)
 *
 * The asset-API tests hit the MCP directly and never need a browser.
 * The filter-UI tests use Playwright's browser engine against the Astro site.
 */

import { test, expect, request } from '@playwright/test';

// ─── helpers ─────────────────────────────────────────────────────────────────

const MCP  = 'http://localhost:8080';
const SITE = 'http://localhost:4321';

/** Fetch the MCP /api/assets endpoint and return parsed JSON */
async function fetchAssets() {
  const ctx = await request.newContext();
  const res = await ctx.get(`${MCP}/api/assets`);
  expect(res.ok(), `MCP /api/assets returned ${res.status()}`).toBeTruthy();
  return res.json() as Promise<{
    items: AssetItem[];
    local_count: number;
    sharepoint_count: number;
  }>;
}

interface AssetItem {
  source: 'local' | 'sharepoint';
  category: string;
  name: string;
  rel_path: string;
  url: string;
  download_url?: string;
  size_bytes?: number;
  variant?: string;
  color?: string;
  format?: string;
  resolution?: string;
}

// ─── MCP API tests ────────────────────────────────────────────────────────────

test.describe('MCP /api/assets — shape & health', () => {
  test('health endpoint returns ok', async ({ request }) => {
    const res = await request.get(`${MCP}/api/health`);
    expect(res.ok()).toBeTruthy();
    const body = await res.json();
    expect(body.status).toBe('ok');
  });

  test('returns items array with counts', async () => {
    const data = await fetchAssets();
    expect(Array.isArray(data.items)).toBeTruthy();
    expect(data.items.length).toBeGreaterThan(0);
    expect(typeof data.local_count).toBe('number');
    expect(typeof data.sharepoint_count).toBe('number');
    expect(data.local_count + data.sharepoint_count).toBe(data.items.length);
  });

  test('every item has required fields', async () => {
    const { items } = await fetchAssets();
    for (const a of items) {
      expect(a.source, `${a.name} missing source`).toMatch(/^(local|sharepoint)$/);
      expect(a.category, `${a.name} missing category`).toBeTruthy();
      expect(a.name, `item missing name`).toBeTruthy();
      expect(a.url, `${a.name} missing url`).toBeTruthy();
    }
  });

  test('expected categories are present', async () => {
    const { items } = await fetchAssets();
    const cats = new Set(items.map(a => a.category));
    for (const expected of ['logo', 'illustration', 'icon', 'image', 'template', 'product-render', 'doc']) {
      expect(cats.has(expected), `category "${expected}" missing`).toBeTruthy();
    }
  });
});

// ─── Category item-count sanity checks ───────────────────────────────────────

test.describe('MCP /api/assets — per-category counts', () => {
  let items: AssetItem[];
  test.beforeAll(async () => {
    ({ items } = await fetchAssets());
  });

  const minimums: Record<string, number> = {
    logo:            100,
    illustration:     10,
    icon:             30,
    image:           100,
    template:         30,
    'product-render': 50,
    doc:               3,
  };

  for (const [cat, min] of Object.entries(minimums)) {
    test(`${cat} has ≥ ${min} items`, () => {
      const count = items.filter(a => a.category === cat).length;
      expect(count, `${cat}: got ${count}, expected ≥ ${min}`).toBeGreaterThanOrEqual(min);
    });
  }
});

// ─── Logo metadata tests ──────────────────────────────────────────────────────

test.describe('MCP /api/assets — logo metadata', () => {
  let logos: AssetItem[];
  test.beforeAll(async () => {
    const { items } = await fetchAssets();
    logos = items.filter(a => a.category === 'logo');
  });

  test('logos have variant field', () => {
    const withVariant = logos.filter(a => a.variant);
    expect(withVariant.length).toBeGreaterThan(0);
  });

  test('logos have color field', () => {
    const withColor = logos.filter(a => a.color);
    expect(withColor.length).toBeGreaterThan(0);
  });

  test('logo colors are valid', () => {
    const validColors = new Set(['purple', 'black', 'blue', 'white']);
    for (const logo of logos.filter(a => a.color)) {
      expect(validColors.has(logo.color!), `unexpected logo color: ${logo.color}`).toBeTruthy();
    }
  });

  test('logo formats include png, svg, eps', () => {
    const formats = new Set(logos.filter(a => a.format).map(a => a.format!));
    expect(formats.has('png')).toBeTruthy();
    expect(formats.has('svg')).toBeTruthy();
  });
});

// ─── Product render path-structure tests ─────────────────────────────────────

test.describe('MCP /api/assets — product-render path structure', () => {
  let renders: AssetItem[];
  test.beforeAll(async () => {
    const { items } = await fetchAssets();
    renders = items.filter(a => a.category === 'product-render');
  });

  function parseRender(a: AssetItem) {
    const parts = a.rel_path.replace(/\\/g, '/').split('/');
    const idx = parts.findIndex(p => /product.?render/i.test(p));
    if (idx < 0) return null;
    return {
      sku:        (parts[idx + 1] || '').trim(),
      formFactor: (parts[idx + 2] || '').trim(),
      label:      (parts[idx + 3] || '').trim(),
      format:     (parts[idx + 4] || '').trim(),
      shadow:     (parts[idx + 5] || '').trim(),
    };
  }

  test('all renders have parseable path structure', () => {
    const unparseable = renders.filter(a => parseRender(a) === null);
    expect(unparseable.length, `${unparseable.length} renders have no "Product Renders" in path`).toBe(0);
  });

  test('render SKUs are from expected set', () => {
    const validSKUs = new Set(['D7-P5520', 'D7-PS1010', 'D7-PS1030']);
    const skus = new Set(renders.map(a => parseRender(a)?.sku).filter(Boolean));
    for (const sku of skus) {
      expect(validSKUs.has(sku!), `unexpected SKU: ${sku}`).toBeTruthy();
    }
  });

  test('render form factors are from expected set', () => {
    const validFF = new Set(['E1.L', 'E1.S - 9.5mm', 'E3.S', 'U.2']);
    const ffs = new Set(renders.map(a => parseRender(a)?.formFactor).filter(Boolean));
    for (const ff of ffs) {
      expect(validFF.has(ff!), `unexpected form factor: ${ff}`).toBeTruthy();
    }
  });

  test('renders have label "With Label" or "Without Label"', () => {
    const labels = new Set(renders.map(a => parseRender(a)?.label).filter(Boolean));
    expect(labels.has('With Label') || labels.has('Without Label')).toBeTruthy();
  });

  test('renders have download_url for direct access', () => {
    const missing = renders.filter(a => !a.download_url);
    expect(missing.length, `${missing.length} product renders missing download_url`).toBe(0);
  });

  test('renders are image files (jpg or png)', () => {
    for (const a of renders) {
      expect(a.name, `render is not an image: ${a.name}`).toMatch(/\.(jpg|jpeg|png)$/i);
    }
  });
});

// ─── SharePoint items quality checks ─────────────────────────────────────────

test.describe('MCP /api/assets — SharePoint item quality', () => {
  let spItems: AssetItem[];
  test.beforeAll(async () => {
    const { items } = await fetchAssets();
    spItems = items.filter(a => a.source === 'sharepoint');
  });

  test('SharePoint items have download_url', () => {
    const missing = spItems.filter(a => !a.download_url);
    // Allow up to 2% missing (some edge cases)
    const pct = missing.length / spItems.length;
    expect(pct, `${missing.length} SP items missing download_url (${(pct*100).toFixed(1)}%)`).toBeLessThan(0.02);
  });

  test('SharePoint urls are absolute https URLs', () => {
    for (const a of spItems) {
      expect(a.url, `${a.name} url is not https`).toMatch(/^https?:\/\//);
    }
  });

  test('image category items are image file types', () => {
    const images = spItems.filter(a => a.category === 'image');
    for (const a of images) {
      expect(a.name, `image category item is not an image: ${a.name}`)
        .toMatch(/\.(jpg|jpeg|png|gif|webp|svg)$/i);
    }
  });
});

// ─── Filter UI tests (requires Astro dev server on :4321) ─────────────────────

test.describe('Assets page — filter UX', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(`${SITE}/assets/`);
    // Wait for the grid to populate (MCP response)
    await page.waitForSelector('.asset-card', { timeout: 15000 });
  });

  test('only Search visible when "All" category selected', async ({ page }) => {
    await page.selectOption('#assetCategory', '');
    await expect(page.locator('#colorField')).toBeHidden();
    await expect(page.locator('#variantField')).toBeHidden();
    await expect(page.locator('#logoFormatField')).toBeHidden();
    await expect(page.locator('#imageSubcatField')).toBeHidden();
    await expect(page.locator('#skuField')).toBeHidden();
    await expect(page.locator('#formFactorField')).toBeHidden();
    await expect(page.locator('#labelField')).toBeHidden();
    await expect(page.locator('#imageFormatField')).toBeHidden();
    await expect(page.locator('#shadowField')).toBeHidden();
    await expect(page.locator('#templateTypeField')).toBeHidden();
  });

  test('logo category shows Color + Variant + Format filters only', async ({ page }) => {
    await page.selectOption('#assetCategory', 'logo');
    await expect(page.locator('#colorField')).toBeVisible();
    await expect(page.locator('#variantField')).toBeVisible();
    await expect(page.locator('#logoFormatField')).toBeVisible();
    // Product-render + template + image fields must stay hidden
    await expect(page.locator('#skuField')).toBeHidden();
    await expect(page.locator('#imageSubcatField')).toBeHidden();
    await expect(page.locator('#templateTypeField')).toBeHidden();
  });

  test('product-render shows 5 sub-filters, hides logo/image/template fields', async ({ page }) => {
    await page.selectOption('#assetCategory', 'product-render');
    await expect(page.locator('#skuField')).toBeVisible();
    await expect(page.locator('#formFactorField')).toBeVisible();
    await expect(page.locator('#labelField')).toBeVisible();
    await expect(page.locator('#imageFormatField')).toBeVisible();
    await expect(page.locator('#shadowField')).toBeVisible();
    await expect(page.locator('#colorField')).toBeHidden();
    await expect(page.locator('#variantField')).toBeHidden();
    await expect(page.locator('#logoFormatField')).toBeHidden();
    await expect(page.locator('#imageSubcatField')).toBeHidden();
    await expect(page.locator('#templateTypeField')).toBeHidden();
  });

  test('image category shows Subject filter only', async ({ page }) => {
    await page.selectOption('#assetCategory', 'image');
    await expect(page.locator('#imageSubcatField')).toBeVisible();
    await expect(page.locator('#colorField')).toBeHidden();
    await expect(page.locator('#skuField')).toBeHidden();
    await expect(page.locator('#templateTypeField')).toBeHidden();
  });

  test('template category shows Type filter only', async ({ page }) => {
    await page.selectOption('#assetCategory', 'template');
    await expect(page.locator('#templateTypeField')).toBeVisible();
    await expect(page.locator('#colorField')).toBeHidden();
    await expect(page.locator('#skuField')).toBeHidden();
    await expect(page.locator('#imageSubcatField')).toBeHidden();
  });

  for (const cat of ['illustration', 'icon', 'doc']) {
    test(`${cat} category shows only Search (no sub-filters)`, async ({ page }) => {
      await page.selectOption('#assetCategory', cat);
      await expect(page.locator('#colorField')).toBeHidden();
      await expect(page.locator('#skuField')).toBeHidden();
      await expect(page.locator('#imageSubcatField')).toBeHidden();
      await expect(page.locator('#templateTypeField')).toBeHidden();
    });
  }

  test('logo color filter reduces results', async ({ page }) => {
    await page.selectOption('#assetCategory', 'logo');
    await page.waitForSelector('.asset-card');
    const allCount = await page.locator('.asset-card').count();

    await page.selectOption('#assetColor', 'purple');
    await page.waitForTimeout(300);
    const purpleCount = await page.locator('.asset-card').count();

    expect(purpleCount).toBeGreaterThan(0);
    expect(purpleCount).toBeLessThanOrEqual(allCount);
  });

  test('product-render SKU filter narrows results', async ({ page }) => {
    await page.selectOption('#assetCategory', 'product-render');
    await page.waitForSelector('.asset-card');
    const allCount = await page.locator('.asset-card').count();

    await page.selectOption('#assetSku', 'D7-PS1010');
    await page.waitForTimeout(300);
    const skuCount = await page.locator('.asset-card').count();

    expect(skuCount).toBeGreaterThan(0);
    expect(skuCount).toBeLessThanOrEqual(allCount);
  });

  test('template type filter narrows results', async ({ page }) => {
    await page.selectOption('#assetCategory', 'template');
    await page.waitForSelector('.asset-card');

    await page.selectOption('#assetTemplateType', 'teams');
    await page.waitForTimeout(300);
    const count = await page.locator('.asset-card').count();
    expect(count).toBeGreaterThan(0);
  });

  test('search filter works across all categories', async ({ page }) => {
    await page.fill('#assetSearch', 'solidigm');
    await page.waitForTimeout(300);
    const count = await page.locator('.asset-card').count();
    expect(count).toBeGreaterThan(0);
    // All visible card names should contain the search term (case-insensitive)
    const names = await page.locator('.asset-card__name').allTextContents();
    for (const name of names) {
      expect(name.toLowerCase()).toContain('solidigm');
    }
  });

  test('switching categories resets sub-filter influence', async ({ page }) => {
    // Set product-render with SKU filter
    await page.selectOption('#assetCategory', 'product-render');
    await page.waitForSelector('.asset-card');
    await page.selectOption('#assetSku', 'D7-PS1010');
    await page.waitForTimeout(200);

    // Switch to logos — SKU field should be hidden, logos should render
    await page.selectOption('#assetCategory', 'logo');
    await page.waitForTimeout(300);
    await expect(page.locator('#skuField')).toBeHidden();
    expect(await page.locator('.asset-card').count()).toBeGreaterThan(0);
  });
});
