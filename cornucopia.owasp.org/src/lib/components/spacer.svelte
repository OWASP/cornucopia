<script lang="ts">
	interface Props {
		height?: string;
	}

	let { _height = '5rem' }: Props = $props();
</script>

<div class="spacer" ></div>

<style>
	.spacer {
		width: 100%;
		height: 5rem;
	}
</style>
