<script>
    import Author from "$lib/components/author.svelte";
import { Text } from "$lib/utils/text";

    export let data;
</script>

<h1>Authors</h1>

<div class="container">
    {#each data.authors as author}
        <Author {author}></Author>
    {/each}
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
        .container
        {
            justify-content: center;
            flex-direction: column;
            margin:auto;
        } 
    }
</style>