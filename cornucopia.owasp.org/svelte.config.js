import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import { config } from 'dotenv';
import { getSvelteEntries, getAppConfig } from './script/app-config.js';
config();

const { svelte: svelteConfig } = getAppConfig();
const cardEntries = svelteConfig.prerendered;

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
                        concurrency: 1,
                        handleHttpError: ({ status, path, referrer, referenceType, message }) => {
                                console.error(
                                        `\n[prerender error] HTTP ${status} on ${path}\n` +
                                        `  Referrer: ${referrer ?? '(direct entry)'}\n` +
                                        `  Reference Type: ${referenceType}\n` +
                                        `  Message: ${message}\n`
                                );

                                const errorCategory =
                                        status >= 500
                                                ? 'Prerender SSR failure'
                                                : status === 404
                                                        ? 'Prerender route not found'
                                                        : 'Prerender HTTP error';

                                const linkedFrom = referrer ? ` (linked from ${referrer})` : '';
                                throw new Error(`${errorCategory} (HTTP ${status}) on ${path}${linkedFrom}: ${message}`);
                        },
                        handleMissingId: ({ _path, id, _referrers, message }) => {
                         if (id == 'card') return;
                         throw new Error(message);
                        },
                        entries: getSvelteEntries(cardEntries)
                },
                csrf: {
                        trustedOrigins: ['https://owaspcornucopia.org', 'https://cornucopia.owasp.org']
                }
        }
};