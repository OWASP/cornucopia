<script lang="ts">
    import SvelteMarkdown from "svelte-markdown";
    import { renderersForGeneralUse } from '$lib/components/renderers/renderers';
    import type { Card } from "../../domain/card/card";
    import { contentLang, getDirection } from "$lib/utils/direction";
    interface Props {
        card: Card;
    }

    let { card }: Props = $props();
    const lang = $derived(contentLang(card.language));
</script>

<div lang={lang} dir={getDirection(lang)}>
    <SvelteMarkdown renderers={renderersForGeneralUse} source={card.concept}></SvelteMarkdown>
</div>
