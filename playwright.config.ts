import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright configuration for Solidigm Brand MCP + Assets page tests.
 *
 * API tests (MCP server on :8080) run without a browser — they use the
 * request fixture which doesn't require a page.
 *
 * UI tests require the Astro site to be running on :4321.
 * Start it with:  cd site && npm run dev
 */
export default defineConfig({
  testDir: './tests',
  fullyParallel: false,
  retries: 1,
  reporter: [['list'], ['html', { open: 'never' }]],

  use: {
    baseURL: 'http://localhost:4321',
    trace: 'on-first-retry',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  // Do NOT auto-start servers here — MCP and Astro should be running already.
  // Run `cd site && npm run dev` and `cd brand_mcp && python -m brand_mcp.server`
});
