<script lang="ts">
    import SvelteMarkdown from "svelte-markdown";
    import renderers from "$lib/components/renderers/renderers"
    import type { Card } from "../../domain/card/card";
    export let card : Card
</script>

<div>
    <SvelteMarkdown {renderers} source={card.summary}></SvelteMarkdown>
</div>