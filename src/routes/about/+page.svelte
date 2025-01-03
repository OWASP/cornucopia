<script>
    import SvelteMarkdown from 'svelte-markdown'
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
    img
    {
        width : 60%;
        margin-left:20%;
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

            img
            {
                width : calc(100% - 4rem);
                margin-left: 2rem
            }
        }
    a,p
    {
        font-size: 1.3rem;
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
