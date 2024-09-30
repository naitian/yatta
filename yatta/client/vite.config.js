import { svelte } from '@sveltejs/vite-plugin-svelte';
import { defineConfig } from 'vite';

import postcss from './postcss.config.js';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  if (mode === 'jupyter') {
    return {
      plugins: [svelte({ hot: false, emitCss: true })],
      css: {
        postcss
      },
      build: {
        sourcemap: true,
        outDir: "./jupyter",
        lib: {
          entry: ["src/jupyter.js"],
          formats: ["es"],
        }
      }
    }
  } else {
    return {
      plugins: [svelte()],
      css: {
        postcss
      },
      server: {
        proxy: {
          '/api': 'http://localhost:4123',
          '/hmr': {
            target: 'ws://localhost:4123',
            ws: true,
            rewriteWsOrigin: true
          },
          '/openapi.json': 'http://localhost:4123',
          '/plugins': 'http://localhost:4123',
          '/docs': 'http://localhost:4123',
          '/redocs': 'http://localhost:4123',
          '/files': 'http://localhost:4123',
        }
      },
    }
  }
})
