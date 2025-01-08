<script>
    import { Text } from '$lib/utils/text';
    import SvelteMarkdown from 'svelte-markdown'
    import renderers from '$lib/components/renderers/renderers';
    import ViewSourceOnGithub from "$lib/components/viewSourceOnGithub.svelte"
    import Utterances from "$lib/components/utterances.svelte"
    /** @type {{data: any}} */
    let { data } = $props();
</script>
<h1 class="clickable" id="{data.title}">{Text.FormatPlain(data.title)}</h1>
<div>
<!--The location is a file -->
{#each data.files as file}
    <p>├──<a href="/taxonomy/{data.path}/{file}">{Text.FormatPlain(file)}</a></p>
{/each}

<!--The location is a folder -->
{#each data.folders as folder}
    <p>├──<a href="/taxonomy/{data.path}/{folder}">{Text.FormatPlain(folder)}</a></p>
{/each}

<!--The location is filecontent -->
{#if data.content && data.content != ''}
    <SvelteMarkdown {renderers} source={data.content}></SvelteMarkdown>
    <ViewSourceOnGithub path={'./data/taxonomy/' + data.path + '/index.md'} ></ViewSourceOnGithub>
    <Utterances name={data.path} ></Utterances>
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