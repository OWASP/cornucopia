<script>
    import SvelteMarkdown from 'svelte-markdown';
    import { renderers }  from '$lib/components/renderers/renderers';
    import {readLang, readTranslation} from "$lib/stores/stores";

    export let data;
    let t = readTranslation();
    const lang = readLang();
    let content = data.content.get($lang) || data.content.get('en');
</script>
<div>
{#if content != ''}
<SvelteMarkdown {renderers} source={content}></SvelteMarkdown>
{/if}
</div>
<style>
    @media (max-width: 767px)
    {
        div
        {
            margin: 0rem 1rem;
        }
    }
</style>
