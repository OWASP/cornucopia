<script>
    import SvelteMarkdown from 'svelte-markdown';
    import renderers from '$lib/components/renderers/renderers';
    import {readLang} from "$lib/stores/stores";

    export let data;
    const lang = readLang();
    let content = data.content.get($lang) || data.content.get('en');
</script>
{#if content != ''}
<SvelteMarkdown {renderers} source={content}></SvelteMarkdown>
{/if}
<style>
    h2,h3
    {
        font-weight: bold;
    }

    div
    {
        font-size: 1.2rem;
    }   

    @media (max-aspect-ratio: 1/1)
    {
        div
        {
            width : 100%;
        }
    }
        a,p
    {
        font-size: 1.2rem;
        font-family: var(--font-body);
    }

    a
    {
        display: inline-block;
        text-decoration: none;
        font-weight: bold;
        color:var(--background);
    }

    a:hover
    {
        opacity: 70%;
        color: rgb(41, 0, 176);
    }
</style>