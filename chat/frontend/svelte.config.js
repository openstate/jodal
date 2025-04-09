import adapter from '@sveltejs/adapter-node';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter({
			out: 'build',
	precompress: false,
			env: {
				dir: '.',
				publicPrefix: 'PUBLIC_'
			}
		}),
		alias: {
			$lib: 'src/lib'
		},
		env: {
			dir: '.',
			publicPrefix: 'PUBLIC_'
		}
	}
};

export default config;
