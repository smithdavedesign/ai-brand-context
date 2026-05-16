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

// GitHub Pages serves from /repo-name/ unless a custom domain is set.
// Vercel and local dev serve from /.
const base = process.env.GITHUB_ACTIONS === 'true' ? '/ai-brand-context/' : '/';

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
