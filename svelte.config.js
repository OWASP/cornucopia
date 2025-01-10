import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = 
{
	preprocess: vitePreprocess(),
	kit: 
	{
		adapter: adapter(),
		alias: {
			$data: "data",
		},
		prerender: {
			handleHttpError: ({ path, referrer, message }) => {
				console.log(message);
				console.log(referrer);
				console.log(path);
				// otherwise fail the build
				throw new Error(message);
			}
		},
		csp: {
			mode: "auto",
			directives: {
				'script-src': ['self'],
				'script-src-elem': ['self']
			},
			reportOnly: {
				'script-src': ['self'],
				'script-src-elem': ['self'],
				'report-uri': ['/']
			}
		},
		csrf: {
			checkOrigin: true
		}
	}
};

export default config;
