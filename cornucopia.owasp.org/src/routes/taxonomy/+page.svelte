<script>
    import { Text } from "$lib/utils/text";
    import { resolve } from "$app/paths";
    import {readLang, readTranslation} from "$lib/stores/stores";
    import { renderersForGeneralUse } from '$lib/components/renderers/renderers';
    import SvelteMarkdown from "svelte-markdown";
    /** @type {{data: any}} */
    let { data } = $props();
    let t = readTranslation();
    const lang = readLang();
    let content = $derived(data.content.get($lang) || data.content.get('en'));
</script>
<div>
{#if content != ''}
    <SvelteMarkdown renderers={renderersForGeneralUse} source={content}></SvelteMarkdown>
{/if}
{#each data.categories as category (category)}
    <p>â”œâ”€â”€<a title="{Text.Format(category)}" href={resolve('/taxonomy/' + category.toLowerCase())}>{Text.Format(category)}</a></p>
{/each}
</div>
<style>
    p
    {
        margin:0;
    }

    a
    {
        text-decoration: none;
        font-weight: bold;
        color:var(--background);
        transition: var(--transition);
    }

    a:hover
    {
        opacity:50%;
    }
    @media (max-width: 767px)
    {
        div
        {
            margin: 0rem 1rem;
        }
    }
</style>

