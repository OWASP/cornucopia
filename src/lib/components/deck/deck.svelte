<script lang="ts">
    import { onMount } from "svelte";
	import { fly } from 'svelte/transition';
    import Card from "./card.svelte";

    let images = 
    [
        "/images/front-page-cards/card-authorization-7.png",
        "/images/front-page-cards/card-cornucopia-8.png",
        "/images/front-page-cards/card-cryptography-k.png",
        "/images/front-page-cards/card-data-validation-and-encoding-Q.png",
        "/images/front-page-cards/card-session-management-5.png",
        "/images/front-page-cards/card-wild-card-joker-b.png",
        "/images/front-page-cards/card-authentication-3.png",
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
        {#each images as image,index}
            <Card {image} {index} {reset}></Card>
        {/each}
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


