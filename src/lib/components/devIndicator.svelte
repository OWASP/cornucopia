<script lang="ts">
    import { page } from "$app/stores";
    let visible : boolean = true;
</script>

{#if visible}
    <button style="{$page.url.hostname == 'localhost' ? '' : 'display:none;'}" on:click={()=>visible=false}>
        <p>Development</p>
    </button>
{/if}

<style>
    button
    {
        background: none;
        background-color: var(--background);
        position: fixed;
        left : 1rem;
        bottom: 1rem;
        z-index: 100;
        padding: .5rem;
        border-radius: 1rem;
        color:var(--green);
        box-shadow: 0px 0px 10px 1px var(--green);
        cursor:pointer;
        border:none;
    }

    button:hover
    {
        box-shadow: 0px 0px 1px 1px var(--green);

    }
</style>