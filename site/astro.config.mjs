// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

// Resolve canonical site URL — Vercel injects these on every build.
const siteUrl = process.env.VERCEL_PROJECT_PRODUCTION_URL
  ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}`
  : process.env.VERCEL_URL
  ? `https://${process.env.VERCEL_URL}`
  : 'http://localhost:4321';

export default defineConfig({
  site: siteUrl,
  base: '/',
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
