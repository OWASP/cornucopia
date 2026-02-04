import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';
import VitePluginRestart from 'vite-plugin-restart';
import { viteStaticCopy } from 'vite-plugin-static-copy'
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

let vitePluginRestartOptions = {restart: ['./data/**']}

// This copies the content from the filesystem data folder to the static file location under '/data/' available at runtime.
// Also copies to server output for prerendering
let viteStaticCopyTargets = [
	{src: './data/**/*', dest: './data/'},
	{src: './data/**/*', dest: '../server/data/'}
]
let viteStaticCopyOptions = { targets: viteStaticCopyTargets}

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
	],
	test: {
		   environment: 'jsdom',
    coverage: {
      provider: 'istanbul',
      reporter: ['cobertura'],
      reportsDirectory: 'coverage',
      exclude: ['node_modules/', '.svelte-kit/']
	}
}
});
