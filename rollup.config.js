import svelte from 'rollup-plugin-svelte';
import replace from '@rollup/plugin-replace';
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import postcss from 'rollup-plugin-postcss';
import livereload from 'rollup-plugin-livereload';
import { terser } from 'rollup-plugin-terser';

const production = !process.env.ROLLUP_WATCH;

function serve() {
	let server;

	function toExit() {
		if (server) server.kill(0);
	}

	return {
		writeBundle() {
			if (server) return;
			server = require('child_process').spawn('npm', ['run', 'start', '--', '--dev'], {
				stdio: ['ignore', 'inherit', 'inherit'],
				shell: true
			});

			process.on('SIGTERM', toExit);
			process.on('exit', toExit);
		}
	};
}

export default {
	input: 'src/main.js',
	output: {
		sourcemap: true,
		format: 'iife',
		name: 'app',
		file: 'public/build/bundle.js'
	},
	plugins: [
		svelte({
			// enable run-time checks when not in production
			dev: !production,
			// we'll extract any component CSS out into
			// a separate file - better for performance
			emitCss: false,
			// Extract CSS into a single bundled file (recommended).
      // See note below
      css: function (css) {
        // creates `main.css` and `main.css.map`
        // using a falsy name will default to the bundle name
        // — pass `false` as the second argument if you don't want the sourcemap
        css.write('bundle.css');
      },
		}),

		replace({
			// 2 level deep object should be stringify
			runEnvironment: JSON.stringify({
				env: {
					isProduction: production,
					googleClientId: production ? '261459702447-d87efq1lonucth8etg8bebgikrsccvus.apps.googleusercontent.com' : '261459702447-7irhrdbh5ib31tif0s0gkchcqhn8t259.apps.googleusercontent.com'
				}
			}),
		}),

		// If you have external dependencies installed from
		// npm, you'll most likely need these plugins. In
		// some cases you'll need additional configuration -
		// consult the documentation for details:
		// https://github.com/rollup/plugins/tree/master/packages/commonjs
		resolve({
			browser: true,
			dedupe: ['svelte']
		}),
		commonjs(),
		postcss({
					extensions: ['.scss', '.sass'],
		      extract: false,
		      minimize: true,
		      use: [
		        ['sass', {
		          includePaths: [
		            './theme',
		            './node_modules'
		          ]
		        }]
		      ]
		    }),
		// In dev mode, call `npm run start` once
		// the bundle has been generated
		!production && serve(),

		// Watch the `public` directory and refresh the
		// browser on changes when not in production
		!production && livereload('public'),

		// If we're building for production (npm run build
		// instead of npm run dev), minify
		//production && terser()
	],
	watch: {
		clearScreen: false
	}
};
