// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://solidigm.github.io',
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
