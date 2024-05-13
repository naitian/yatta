import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		proxy: {
			'/api': 'http://localhost:4123',
			'/plugins': 'http://localhost:4123',
			'/docs': 'http://localhost:4123',
			'/files': 'http://localhost:4123',
		}
	}
});
