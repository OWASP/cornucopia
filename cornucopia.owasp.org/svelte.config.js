import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import { config } from 'dotenv';
config();
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

if (JSON.stringify(process.env.VERCEL_ENV) == 'preview') {
	csp = {
		mode: "hash",
		directives: {
			'default-src': ['none'],
			'connect-src': ['self', 'https://vercel.live/', 'https://vercel.com', '*.pusher.com', '*.pusherapp.com'],
			'script-src': ['self', 'https://vercel.live/', 'https://vercel.com', 'unsafe-inline'],
			'script-src-elem': ['self', 'https://vercel.live/', 'https://vercel.com'],
			'style-src': ['self'],
			'style-src-elem': ['self'],
			'img-src': ['self', 'https://i.ytimg.com/vi/XXTPXozIHow/mqdefault.jpg', 'https://vercel.live/', 'https://vercel.com', '*.pusher.com/', 'data: blob'],
			'frame-src': ['self', 'https://www.youtube.com/', 'https://vercel.live/', 'https://vercel.com']
		},
		
	};
}

export default {
	preprocess: vitePreprocess(),
	kit: 
	{
		adapter: adapter({
			routes: {
				include: ['/*'],
				exclude: ["/build/*"]
			},
			fallback: '/error'
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
			},
			handleMissingId: ({ path, id, referrers, message }) => {
			 if (id == 'card') return;
			 throw new Error(message);
			},
			entries: [
				'/cards/ACA',
				'/cards/AC2',
				'/cards/AC3',
				'/cards/AC4',
				'/cards/AC5',
				'/cards/AC6',
				'/cards/AC7',
				'/cards/AC8',
				'/cards/AC9',
				'/cards/ACX',
				'/cards/ACJ',
				'/cards/ACQ',
				'/cards/ACK',
				'/cards/COA',
				'/cards/CO2',
				'/cards/CO3',
				'/cards/CO4',
				'/cards/CO5',
				'/cards/CO6',
				'/cards/CO7',
				'/cards/CO8',
				'/cards/CO9',
				'/cards/COX',
				'/cards/COJ',
				'/cards/COQ',
				'/cards/COK',
				'/cards/COMA',
				'/cards/COM2',
				'/cards/COM3',
				'/cards/COM4',
				'/cards/COM5',
				'/cards/COM6',
				'/cards/COM7',
				'/cards/COM8',
				'/cards/COM9',
				'/cards/COMX',
				'/cards/COMJ',
				'/cards/COMQ',
				'/cards/COMK',
				'/cards/DVEA',
				'/cards/DVE2',
				'/cards/DVE3',
				'/cards/DVE4',
				'/cards/DVE5',
				'/cards/DVE6',
				'/cards/DVE7',
				'/cards/DVE8',
				'/cards/DVE9',
				'/cards/DVEX',
				'/cards/DVEJ',
				'/cards/DVEQ',
				'/cards/DVEK',

				'/404'
			]
		},
		//csp: csp,
		csrf: {
			checkOrigin: true
		}
	}
};
