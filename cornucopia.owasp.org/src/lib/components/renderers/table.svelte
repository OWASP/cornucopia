<script>
    /** @type {{children?: import('svelte').Snippet}} */
    let { children } = $props();
</script>

<table>
    {#if children}{@render children()}{/if}
    
</table>


<style>
    table
    {
        margin:auto;
        border-radius: .25rem;
        margin-top: 2rem;
        box-shadow: var(--box-shadow);
        border-collapse: collapse;
        overflow: hidden;
    }

    @media (max-aspect-ratio: 1/1) 
    {
        table
        {
            width: 100%;
        }
    }
</style>