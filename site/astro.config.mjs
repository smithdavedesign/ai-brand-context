// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';

export default defineConfig({
  site: 'https://solidigm.github.io',
  base: '/',
  outDir: './dist',
  integrations: [mdx()],
  vite: {
    resolve: {
      alias: {
        '@tokens': '/../tokens',
      },
    },
  },
});
