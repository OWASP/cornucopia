<script>
    /** @type {{children?: import('svelte').Snippet}} */
    let { children } = $props();
</script>

<p>{@render children?.()}</p>

<style>
    p
    {
        text-align: left;
        font-weight: 400;
        font-size: 1.2rem;
        opacity: 90%;
        font-family: var(--font-body);
        margin-top: 0;
    }
</style>