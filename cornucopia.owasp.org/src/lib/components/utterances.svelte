<script lang="ts">
import { onMount } from 'svelte';
let loading: boolean = $state(true);
let percentage: number = $state(0);
let scriptReady: boolean = $state(false);

interface Props {
name: string;
delay?: number;
}

let { name, delay = 250 }: Props = $props();

onMount(async () => {
for (let i = 0; i < 10; i++) {
await new Promise((resolve) => setTimeout(resolve, delay));
percentage += 10;
}
loading = false;
scriptReady = true;
});
</script>

<div>
{#if scriptReady}
<script
src="https://utteranc.es/client.js"
repo="OWASP/cornucopia"
issue-term={name}
theme="github-light"
label="Utterances"
crossorigin="anonymous"
async
></script>
{/if}
</div>
{#if loading}
<p>Loading comments {percentage}%</p>
{/if}

<style>
div {
min-height: 13rem;
}

p {
color: var(--white);
font-family: var(--font-title);
font-weight: 400;
font-size: 1.5rem;
text-align: center;
}
</style>
