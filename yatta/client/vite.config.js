import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
  server: {
    proxy: {
      '/api': 'http://localhost:4123',
      '/plugins': 'http://localhost:4123',
      '/docs': 'http://localhost:4123',
      '/files': 'http://localhost:4123',
    }
  },
})
