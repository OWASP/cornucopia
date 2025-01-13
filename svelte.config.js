import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = 
{
	preprocess: vitePreprocess(),
	kit: 
	{
		adapter: adapter({
			fallback: '200.html' // may differ from host to host
		}),
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
				'default-src': ['none'],
				'connect-src': ['self'],
				'script-src': ['self'],
				'script-src-elem': ['self'],
				'style-src': ['self'],
				'style-src-elem': ['self'],
				'img-src': ['self', 'https://i.ytimg.com/vi/XXTPXozIHow/mqdefault.jpg'],
				'frame-src': ['self', 'https://www.youtube.com/']
			}
		},
		csrf: {
			checkOrigin: true
		}
	}
};

export default config;
