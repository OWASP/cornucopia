<script>
    import { Text } from '$lib/utils/text';
    import SvelteMarkdown from 'svelte-markdown'
    import renderers from '$lib/components/renderers/renderers';
    import ViewSourceOnGithub from "$lib/components/viewSourceOnGithub.svelte"
    /** @type {{data: any}} */
    let { data } = $props();
</script>
{#if data.folders.length != 0 }
<h1 class="clickable" id="{data.title}">{Text.Format(data.title)}</h1>
{/if}
<div>
<!--The location is a file -->
{#each data.files as file}
    <p>├──<a href="/taxonomy/{data.path.toLowerCase()}/{file.toLowerCase()}">{Text.Format(file)}</a></p>
{/each}

<!--The location is a folder -->
{#each data.folders as folder}
    <p>├──<a href="/taxonomy/{data.path.toLowerCase()}/{folder.toLowerCase()}">{Text.Format(folder)}</a></p>
{/each}

<!--The location is filecontent -->
{#if data.content && data.content != ''}
    <SvelteMarkdown {renderers} source={data.content}></SvelteMarkdown>
    <ViewSourceOnGithub path={'./data/taxonomy/' + data.path + '/index.md'} ></ViewSourceOnGithub>
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