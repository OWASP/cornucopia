<script>
    import Author from "$lib/components/author.svelte";

    import {readTranslation} from "$lib/stores/stores";
    let t = readTranslation();
    /** @type {{data: any}} */
    let { data } = $props();
</script>
<div>
<h1>{$t('news.author.h1')}</h1>

<div class="container">
    {#each data.authors as author}
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

    
    @media (max-aspect-ratio: 1/1) 
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