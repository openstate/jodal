import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig(({ command, mode }) => {
	const config = {
		plugins: [sveltekit()],
		css: {
			postcss: true
		},
		envPrefix: ['PUBLIC_', 'VITE_'],
	};

	if (mode === 'development') {
		config.server = {
			watch: {
				usePolling: true,
				interval: 1000,
			},
			host: true,
			port: 5173,
			proxy: {
				'/api': {
					target: 'http://backend:8000',
					changeOrigin: true,
						secure: false,
				},
			},
		};
	}

	return config;
});