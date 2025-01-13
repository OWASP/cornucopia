<script lang="ts">
	import { onMount } from 'svelte';
	let bindingElement: HTMLElement = $state();
	let loading : boolean = $state(true);
	let percentage : number = $state(0);

	interface Props {
		name: string;
		delay?: number;
	}

	let { name, delay = 250 }: Props = $props();

	onMount(async ()=> createCommentSection())

	
	async function sleep (time : number) 
	{
    	return new Promise((resolve) => setTimeout(resolve, time));
	}


	async function createCommentSection()
	{
		for(let i = 0 ; i < 10 ; i++)
		{
			await sleep(delay);
			percentage += 10
		}

		loading = false;
		let scriptTag = document.createElement('script');
		scriptTag.classList.add("utterances-script")
		scriptTag.setAttribute('id','comment-section')
		scriptTag.setAttribute('repo', 'OWASP/cornucopia');
		scriptTag.setAttribute('issue-term', name);
		scriptTag.setAttribute('theme', 'github-light');
        scriptTag.setAttribute('label', '🔮 Utterances');
		scriptTag.setAttribute('crossorigin', 'anonymous');
		scriptTag.src = 'https://utteranc.es/client.js';

		if(bindingElement)
			bindingElement.appendChild(scriptTag);
	}
</script>

<div bind:this={bindingElement}></div>
{#if loading}
	<p>Loading comments {percentage}%</p>
{/if}

<style>
	div
	{
		min-height: 13rem;
	}

	p
	{
		color: var(--white);
        font-family: var(--font-title);
        font-weight: 400;
		font-size: 1.5rem;
		text-align: center;
	}
</style>