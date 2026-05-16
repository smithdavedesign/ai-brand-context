// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

// Resolve canonical site URL — Vercel injects these on every build.
const siteUrl = process.env.VERCEL_PROJECT_PRODUCTION_URL
  ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}`
  : process.env.VERCEL_URL
  ? `https://${process.env.VERCEL_URL}`
  : process.env.GITHUB_ACTIONS
  ? 'https://smithdavedesign.github.io'
  : 'http://localhost:4321';

// PAGES_BASE can be set per-workflow to control the base path explicitly.
// Falls back to /ai-brand-context/ for GitHub Actions (personal repo) or / everywhere else.
const base = process.env.PAGES_BASE
  ?? (process.env.GITHUB_ACTIONS === 'true' ? '/ai-brand-context/' : '/');

export default defineConfig({
  site: siteUrl,
  base,
  outDir: './dist',
  integrations: [mdx(), sitemap()],
  vite: {
    resolve: {
      alias: {
        '@tokens': '/../tokens',
      },
    },
  },
});
