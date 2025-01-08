<script lang="ts">
	interface Props {
		height?: string;
	}

	let { height = '5rem' }: Props = $props();
</script>

<div style="height:{height}"></div>

<style>
	div {
		width: 100%;
	}
</style>
