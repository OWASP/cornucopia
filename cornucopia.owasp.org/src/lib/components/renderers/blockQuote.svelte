<script>
    /** @type {{children?: import('svelte').Snippet}} */
    let { children } = $props();
</script>

<blockquote>
    <p><b>Note</b></p>
    <div>
        {@render children?.()}
    </div>
</blockquote>


<style>
    blockquote
    {
        border-radius: .5rem;
        background-color: var(--color-note-background);
        text-align: justify;
        font-weight: 300;
        outline : .1rem solid var(--background);
        width: 100%;
        margin:0;
    }

    div
    {
        padding: .25rem;
    }

    p
    {
        background-color: var(--background);
        margin:0;
        color:white;
        padding: .25rem;
        border-top-left-radius: .5rem;
        border-top-right-radius: .5rem;
    }
</style>