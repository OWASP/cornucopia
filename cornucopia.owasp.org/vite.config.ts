import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import VitePluginRestart from 'vite-plugin-restart';
import { viteStaticCopy } from 'vite-plugin-static-copy'

let vitePluginRestartOptions = {restart: ['./data/**']}

// This copies the content from the filesystem data folder to the static file location under '/data/' available at runtime.
let viteStaticCopyTargets = [{src: './data/*',dest: './data/'}]
let viteStaticCopyOptions = { targets: viteStaticCopyTargets}

export default defineConfig({
	test: {
		coverage: {
			enabled: true, 
			provider: 'v8', 
			reporter: ['text', 'json', 'lcov'],
			reportsDirectory: './coverage',
		},
		include: ['**/*.test.ts', '**/*.test.tsx']
	},
	plugins: [
		sveltekit(),
		VitePluginRestart(vitePluginRestartOptions),
		viteStaticCopy(viteStaticCopyOptions)
	]
});
