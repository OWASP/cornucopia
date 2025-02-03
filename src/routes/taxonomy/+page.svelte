<script>
    import { Text } from "$lib/utils/text";

    export let data;
</script>

{#each data.categories as category}
    <p>├──<a href="/taxonomy/{category}">{Text.Format(category)}</a></p>
{/each}

<style>
    p
    {
        font-size: 1.5rem;
        margin:0;
    }

    a
    {
        text-decoration: none;
        font-weight: bold;
        color:var(--background);
        transition: var(--transition);
    }

    a:hover
    {
        opacity:50%;
    }
</style>