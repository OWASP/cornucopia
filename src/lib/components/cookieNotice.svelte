<script lang="ts">
    import { browser } from "$app/environment";

    let noticeAccepted : boolean = false;
    const key : string = 'notice-accepted';
    const value : string = 'true';


    if (browser)
    {
        let storage : boolean =  localStorage.getItem(key) == value;
        if(storage)
            noticeAccepted = true;
    }
    else
    {
        noticeAccepted = true;
    }

    function accept()
    {
        localStorage.setItem(key,value);
        noticeAccepted = true;
    }
</script>

{#if !noticeAccepted}
    <div class="container">
        <div class="left">
            <p>
                This website uses cookies to analyze traffic. We only share this information with our analytics partners.
            </p>
        </div>
        <div class="right">
            <button data-umami-event="cookie-button" on:click={accept}>Accept</button>
        </div>
    </div>
{/if}

<style>
    .container
    {
        display: flex;
        flex-direction: row;
        flex-wrap: nowrap;
        justify-content: space-between;
        position: fixed;
        left : 0;
        bottom: 0;
        z-index: 150;
        padding: .5rem;
        width : 100%;
        background-color: var(--background);
        border-top: 3px var(--white) solid;
    }

    .right
    {
        margin-right: 2rem;
    }

    p
    {
        margin: 1rem;
    }

    button
    {
        border: none;
        color:var(--background);
        background-color: var(--white);
        font-family: var(--font-title);
        padding: 1rem;
        cursor: pointer;
        height : 100%;
    }

    button:hover
    {
        opacity: 80%;
    }
</style>