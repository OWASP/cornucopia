import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import { config } from 'dotenv';
config();

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
			$domain: "src/domain",
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
				'/404',
				'/api/cre/webapp/en',
				'/api/cre/webapp/it',
				'/api/cre/webapp/nl',
				'/api/cre/webapp/es',
				'/api/cre/webapp/fr',
				'/api/cre/webapp/ru',
				'/api/cre/webapp/pt_pt',
				'/api/cre/webapp/pt_br',
				'/api/cre/webapp/no_nb',
				'/api/cre/mobileapp/en',
				'/card/webapp/VE2/2.2/es',
				'/card/webapp/VE2/2.2/it',
				'/card/webapp/VE2/2.2/nl',
				'/card/webapp/VE2/2.2/fr',
				'/card/webapp/VE2/2.2/pt_pt',
				'/card/webapp/VE2/2.2/pt_br',
				'/card/webapp/VE2/2.2/no_nb',
				'/card/webapp/VE2/2.2/ru',
				'/card/webapp/VE2/3.0',
				'/card/webapp/VE2/3.0/en',
				'/card/webapp/VE2/3.0/es',
				'/card/webapp/VE2/3.0/it',
				'/card/webapp/VE2/3.0/nl',
				'/card/webapp/VE2/3.0/fr',
				'/card/webapp/VE2/3.0/pt_pt',
				'/card/webapp/VE2/3.0/pt_br',
				'/card/webapp/VE2/3.0/no_nb',
				'/card/webapp/VE2/3.0/ru',
			]
		},
		csrf: {
			checkOrigin: true
		}
	}
};
