<script>
    import { Text } from "$lib/utils/text";
    import {readLang, readTranslation} from "$lib/stores/stores";
    import renderers from '$lib/components/renderers/renderers';
    import SvelteMarkdown from "svelte-markdown";
    /** @type {{data: any}} */
    let { data } = $props();
    let t = readTranslation();
    const lang = readLang();
    let content = data.content.get($lang) || data.content.get('en');
</script>
<div>
{#if content != ''}
    <SvelteMarkdown {renderers} source={content}></SvelteMarkdown>
{/if}
{#each data.categories as category}
    <p>├──<a href="/taxonomy/{category.toLowerCase()}">{Text.Format(category)}</a></p>
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
    @media (max-aspect-ratio: 1/1)
    {
        div
        {
            margin: 0rem 1rem;
        }
    }
</style>