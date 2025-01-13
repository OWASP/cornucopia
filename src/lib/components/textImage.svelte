<script lang="ts">
	interface Props {
		align?: 'left' | 'right';
		id?: string;
		src: string;
		children?: import('svelte').Snippet;
	}

	let {
		align = 'left',
		id = "",
		src,
		children
	}: Props = $props();

	let innerWidth = $state(0);
	let innerHeight = $state(0);
	let mobile: boolean = $derived(innerWidth / innerHeight < 1);
	
	

	function getFlexStyle(isMobile: boolean) {
		if (isMobile) return '';

		if (align == 'left') {
			return ' desktop-left';
		} else {
			return ' desktop-right';
		}
	}
</script>

<svelte:window bind:innerWidth bind:innerHeight />

{#if id != ""}
	<div class="anchor" id={id}></div>
{/if}
<div class="container{getFlexStyle(mobile)}">
	<div class="image">
        <img alt={id} {src} />
    </div>
	<div class="text{getFlexStyle(mobile)}">
		{@render children?.()}
	</div>
</div>


<style>
	.anchor
	{
		position: absolute;
		height: 1rem;
		transform: translate(0,-4rem);
		width: 1rem;
		pointer-events: none;
	}
	.container {
		width: 90%;
		margin: auto;
		padding: 0rem;
		display: flex;
		display: flex;
		flex-direction: row;
		flex-wrap: nowrap;
		margin-top: 4rem;
	}

	.text {
		outline: 1px rgb(231, 231, 231) solid;
		height: 100%;
		width: calc(50% - 4rem);
		opacity: 80%;
		border-radius: 1rem;
		background-color: rgb(255, 255, 255);
		padding: 1rem 2rem 1rem 1rem;
		box-shadow: var(--box-shadow);
	}

	.text.desktop-left {
		padding: 1rem 1rem 1rem 2rem;
	}

	.text.desktop-right {
		padding: 1rem 2rem 1rem 1rem;
	}

	.image {
		width: 50%;
		text-align: center;
	}

	img {
		width: 80%;
		object-fit: cover;
		border-radius: .3rem;
	}

	.container.desktop-right {
		flex-direction: row-reverse;
	}

	.container.desktop-left {
		flex-direction: row;
	}

	@media (max-aspect-ratio: 1/1) {
		.container {
			flex-direction: column;
		}

		.image {
			width: 90%;
			padding: 0;
			margin: auto;
		}

		.text {
			padding: 1rem;
			height: 100%;
			width: calc(100% - 2rem);
		}
	}
</style>
