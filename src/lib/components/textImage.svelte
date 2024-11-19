<script lang="ts">
	export let align: 'left' | 'right' = 'left';
	export let id : string = "";
	export let src : string;

	let innerWidth = 0;
	let innerHeight = 0;
	let mobile: boolean;
	
	$: {
		mobile = innerWidth / innerHeight < 1;
	}

	function getFlexStyle(isMobile: boolean) {
		if (isMobile) return '';

		if (align == 'left') {
			return 'flex-direction:row ';
		} else {
			return 'flex-direction:row-reverse ';
		}
	}
</script>

<svelte:window bind:innerWidth bind:innerHeight />

{#if id != ""}
	<div class="anchor" id={id}></div>
{/if}
<div class="container" style={getFlexStyle(mobile)}>
	<div class="image">
        <img alt={id} {src} />
    </div>
	<div style="{align == 'left' && !mobile ? 'padding-left:2rem;' : 'padding-right:2rem;'}" class="text">
		<slot />
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
	.last {
		margin-bottom: 1rem;
	}

	.text {
		outline: 1px rgb(231, 231, 231) solid;
		height: 100%;
		width: calc(50% - 4rem);
		opacity: 80%;
		border-radius: 1rem;
		background-color: rgb(255, 255, 255);
		padding: 1rem;
		box-shadow: rgba(255, 255, 255, 0.1) 0px 1px 1px 0px inset, rgba(50, 50, 93, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px;
	}

	.image {
		width: 50%;
		text-align: center;
	}

	img {
		width: 50%;
		object-fit: cover;
		border-radius: .3rem;
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
