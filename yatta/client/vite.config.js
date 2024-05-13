import { svelte } from '@sveltejs/vite-plugin-svelte';
import { defineConfig } from 'vite';

import postcss from './postcss.config.js';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
  css: {
    postcss
  },
  server: {
    proxy: {
      '/api': 'http://localhost:4123',
      '/plugins': 'http://localhost:4123',
      '/docs': 'http://localhost:4123',
      '/files': 'http://localhost:4123',
    }
  },
})
