<script lang="ts">
    import { error } from '@sveltejs/kit';
    import { onMount } from 'svelte';
    import {type Card} from "../../domain/card/card"

	export let card: string;
        export let versions;

	onMount(() => {
        error(404, {
            message: `Unknown card: ${String(card).toUpperCase()}`
        });
    });
</script>

<p>Unknown card: {String(card).toUpperCase()}</p>

<style>
    p {
        color: red;
    }
</style>
