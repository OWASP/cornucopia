<script>
    /** @type {{children?: import('svelte').Snippet}} */
    let { children } = $props();
</script>

<li>{@render children?.()}</li>

<style>
    li
    {
        list-style-position: inside;
    }
</style>