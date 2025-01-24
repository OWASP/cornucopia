<script lang="ts">
    import { browser } from "$app/environment";
    import { goto } from "$app/navigation";
    import { onDestroy } from "svelte";

    // Automatic return to homepage delay in milliseconds
    let timer : number = $state(10000);

    let timeoutId : number = -1;

    start();

    function start()
    {
        timeoutId = +setTimeout(decrementTimer,33);
    }
    
    function decrementTimer()
    {
        if(isLocalDev())
            return;
        
        clearTimeout(timeoutId);
        timer -= 33;
        timeoutId = +setTimeout(decrementTimer,33);
        if(timer < 33)
            goto('/');
    }

    function isLocalDev() : boolean
    {
        if(browser)
            return window.location.host.toLowerCase().includes('localhost');
        else
            return true;
    }

    onDestroy(()=>clearTimeout(timeoutId));
</script>

<div class="error-message">
    <p>Oops, something went wrong!</p>
    {#if !isLocalDev()}
        <p>Returning to <a href="/">landing page</a> in {Math.floor(timer/1000.0)} seconds.</p>
    {/if}
</div>

<style>
    .error-message
    {
        min-height: 80vh;
    }
    p,a
    {
        color: var(--background);
        width : 100%;
        margin:auto;
        text-align: center;
        font-family: var(--font-title);
        font-weight: 400;
        margin-top: 10rem;
    }
</style>