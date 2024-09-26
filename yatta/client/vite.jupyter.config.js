import { svelte } from '@sveltejs/vite-plugin-svelte';
import { defineConfig } from 'vite';

import postcss from './postcss.config.js';

// https://vitejs.dev/config/
export default defineConfig({
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
})
