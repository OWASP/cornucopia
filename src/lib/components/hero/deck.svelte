<script lang="ts">
    import { onMount } from "svelte";

    let images = 
    [
        "/cards/card-authorization-7.png",
        "/cards/card-cornucopia-8.png",
        "/cards/card-cryptography-k.png",
        "/cards/card-data-validation-and-encoding-Q.png",
        "/cards/card-session-management-5.png",
        "/cards/card-wild-card-joker-b.png",
        "/cards/card-authentication-3.png",
    ]

    let visible = false;

    onMount(()=>{visible=true;});
    
    function reset()
    {
        window.scrollTo(0,0);
        images = images.sort((a, b) => 0.5 - Math.random());
        visible = false;
        setTimeout(()=>visible=true,1);
    }
</script>

{#if visible}
    <div class="deck">

    </div>
{/if}


<style>
    .deck
    {
        overflow: hidden;
        width : 100%;
        height : 100%;
    }
</style>


