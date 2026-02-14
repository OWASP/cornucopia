<script>
	export const prerender = false;

	import { onMount } from 'svelte';

	onMount(async () => {
		const SwaggerUIBundle = (await import('swagger-ui-dist/swagger-ui-bundle.js')).default;
		await import('swagger-ui-dist/swagger-ui.css');

		SwaggerUIBundle({
			url: '/api/openapi.yaml',
			dom_id: '#swagger-ui'
		});
	});
</script>

<div id="swagger-ui"></div>

