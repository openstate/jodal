import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],

	server: {
		port: 3000,
		hmr: {
			host: 'app.bron.live'
		},
		fs: {
			allow: [
				'static'
			]
		}
	}

});
