<script>
    import Metadata from "$lib/components/metadata.svelte";
    import { Text } from '$lib/utils/text';
    import { resolve } from '$app/paths';
    import SvelteMarkdown from 'svelte-markdown'
    import { renderers }  from '$lib/components/renderers/renderers';
    import ViewSourceOnGithub from "$lib/components/viewSourceOnGithub.svelte"
    /** @type {{data: any}} */
    let { data } = $props();
</script>
{#if data.metadata}<Metadata metadata={data.metadata} />{/if}
{#if data.categories.length != 0 }
<h1 class="clickable" title="{Text.Format(data.title)}" id="{data.title}">{Text.Format(data.title)}</h1>
{/if}
<div>

<!--The location is a folder -->
{#each data.categories as category (category)}
    <p>ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒâ€¦Ã¢â‚¬Å“ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚ÂÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬<a title="{Text.Format(category)}" href={resolve(data.path + '/' + category.toLowerCase())}>{Text.Format(category)}</a></p>
{/each}

<!--The location is filecontent -->
{#if data.content && data.content != ''}
    <SvelteMarkdown {renderers} source={data.content}></SvelteMarkdown>
    <ViewSourceOnGithub path={data.truePath + '/index.md'} ></ViewSourceOnGithub>
{/if}
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

    h1
    {
        font-weight: bolder;
    }
    .clickable:hover
    {
        opacity: 70%;
        cursor: pointer;
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
