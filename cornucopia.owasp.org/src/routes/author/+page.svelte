<script>
    import Metadata from "$lib/components/metadata.svelte";
    import Author from "$lib/components/author.svelte";

    import {readTranslation} from "$lib/stores/stores";
    let t = readTranslation();
    /** @type {{data: any}} */
    let { data } = $props();
</script>
{#if data.metadata}<Metadata metadata={data.metadata} />{/if}
<div>
<h1>{$t('news.author.h1')}</h1>

<div class="container">
    {#each data.authors as author (author.name)}
        <Author {author}></Author>
    {/each}
</div>
</div>
<style>
    .container
    {
        width : 100%;
        display: flex;
        justify-content: space-between;
        flex-direction: row;
        flex-wrap: wrap;
    }

    
    @media (max-width: 767px) 
    {
        div
        {
            margin: 0rem 1rem;
        }
        .container
        {
            justify-content: center;
            flex-direction: column;
            margin: auto;
        } 
    }
</style>

