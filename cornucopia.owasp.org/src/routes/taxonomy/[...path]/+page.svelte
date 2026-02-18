<script>
    import { Text } from '$lib/utils/text';
    import SvelteMarkdown from 'svelte-markdown'
    import { renderers }  from '$lib/components/renderers/renderers';
    import ViewSourceOnGithub from "$lib/components/viewSourceOnGithub.svelte"
    /** @type {{data: any}} */
    let { data } = $props();
</script>
<svelte:head>
    <link rel="canonical" href="/taxonomy" />
    <title>{data.title}</title>
	<meta name="description" content="{Text.Format(data.title)}" />
	<meta name="keywords" content="cornucopia, threat modeling, taxonomy, requirements" />
    <meta property="og:title" content="{Text.Format(data.title)}">
    <meta property="og:description" content="{Text.Format(data.title)}">
    <meta name="twitter:title" content="{Text.Format(data.title)}">
    <meta name="twitter:description" content="{Text.Format(data.title)}">
</svelte:head>
{#if data.categories.length != 0 }
<h1 class="clickable" title="{Text.Format(data.title)}" id="{data.title}">{Text.Format(data.title)}</h1>
{/if}
<div>

<!--The location is a folder -->
{#each data.categories as category}
    <p>├──<a title="{Text.Format(category)}" href="{data.path}/{category.toLowerCase()}">{Text.Format(category)}</a></p>
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
    @media (max-aspect-ratio: 1/1)
    {
        div
        {
            margin: 0rem 1rem;
        }
    }
    
</style>