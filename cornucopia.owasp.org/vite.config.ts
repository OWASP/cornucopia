import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import VitePluginRestart from 'vite-plugin-restart';
import { viteStaticCopy } from 'vite-plugin-static-copy'
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const vitePluginRestartOptions = {restart: ['./data/**']}

// This copies the content from the filesystem data folder to the static file location under '/data/' available at runtime.
// Also copies to server output for prerendering
const viteStaticCopyTargets = [
	{src: './data/**/*', dest: './data/'},
	{src: './data/**/*', dest: '../server/data/'}
]
const viteStaticCopyOptions = { targets: viteStaticCopyTargets}

export default defineConfig({
	resolve: {
		alias: {
			$lib: path.resolve(__dirname, './src/lib'),
			$domain: path.resolve(__dirname, './src/domain')
		}
	},
	plugins: [
		sveltekit(),
		VitePluginRestart(vitePluginRestartOptions),
		viteStaticCopy(viteStaticCopyOptions)
	]
});
