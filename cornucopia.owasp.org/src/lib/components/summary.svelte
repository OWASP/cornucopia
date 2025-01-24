<script lang="ts">
    import SvelteMarkdown from "svelte-markdown";
    import renderers from "$lib/components/renderers/renderers"
    import type { Card } from "../../domain/card/card";
    interface Props {
        card: Card;
    }

    let { card }: Props = $props();
</script>

<div>
    <SvelteMarkdown {renderers} source={card.summary}></SvelteMarkdown>
</div>