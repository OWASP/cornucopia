import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import { VERCEL_ENV } from '$env/static/private';

let csp = {
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
};

if (VERCEL_ENV == 'preview') {
	csp = {
		mode: "auto",
		directives: {
			'default-src': ['none'],
			'connect-src': ['self', 'https://vercel.live/', 'https://vercel.com', '*.pusher.com', '*.pusherapp.com'],
			'script-src': ['self', 'https://vercel.live/', 'https://vercel.com', 'unsafe-inline'],
			'script-src-elem': ['self', 'https://vercel.live/', 'https://vercel.com'],
			'style-src': ['self'],
			'style-src-elem': ['self'],
			'img-src': ['self', 'https://i.ytimg.com/vi/XXTPXozIHow/mqdefault.jpg', 'https://vercel.live/', 'https://vercel.com', '*.pusher.com/', 'data: blob'],
			'frame-src': ['self', 'https://www.youtube.com/', 'https://vercel.live/', 'https://vercel.com']
		}
	};
}


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
		csp: csp,
		csrf: {
			checkOrigin: true
		}
	}
};

export default config;
