<script>
    import { Text } from "$lib/utils/text";
    import {readLang, readTranslation} from "$lib/stores/stores";
    import renderers from '$lib/components/renderers/renderers';
    import SvelteMarkdown from "svelte-markdown";
    export let data;
    let t = readTranslation();
    const lang = readLang();
    let content = data.content.get($lang) || data.content.get('en');
</script>
<div>
{#if content != ''}
    <SvelteMarkdown {renderers} source={content}></SvelteMarkdown>
{/if}
{#each data.categories as category}
    <p>├──<a href="/taxonomy/{category}">{Text.Format(category)}</a></p>
{/each}
</div>
<style>
    p
    {
        font-size: 1.5rem;
        margin:0;
    }

    div
    {
        font-size: 1.2rem;
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
</style>