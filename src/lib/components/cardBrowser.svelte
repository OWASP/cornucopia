<script lang="ts">
    import CardPreview from "./cardPreview.svelte";
    import { onDestroy } from "svelte";
    import { browser } from "$app/environment";
    import type { Card } from "../../domain/card/card";
    import { goto } from "$app/navigation";
    export let card : Card;
    export let cards : Map<string, Card>;
    export let mappingData : any;
  
    function checkKey(event : any) 
    {
        console.log(event);
        const KEYCODE_RIGHT = 39;
        const KEYCODE_LEFT = 37;
        if(event.keyCode == KEYCODE_RIGHT)
        {
            goto(getNext(card))
        }   

        if(event.keyCode == KEYCODE_LEFT)
        {
            goto(getPrevious(card))
        }
    }

    function getPrevious(card : Card)
    {
        console.log('/' + cards.get(card.prevous)?.suit + '/' + cards.get(card.prevous)?.id + '/#card');
        return '/' + cards.get(card.prevous)?.suit + '/' + cards.get(card.prevous)?.id + '/#card';    
    }

    function getNext(card : Card)
    {
        console.log('/' + cards.get(card.next)?.suit + '/' + cards.get(card.next)?.id + '/#card');
        return '/' + cards.get(card.next)?.suit + '/' + cards.get(card.next)?.id + '/#card';
    }

    onDestroy(()=> {if(browser)document.onkeydown = null})

    if(browser)
        document.onkeydown = checkKey;
</script>

<div class="card-panel" id="card">
    <div class="left" data-umami-event="card-browser-left-button">
        <a href={getPrevious(card)} class="arrow" title="View previous card">{"<"}</a>
    </div>
    <div class="center">
        <CardPreview card={card} mapping={mappingData}></CardPreview>
    </div>
    <div class="right" data-umami-event="card-browser-right-button">
        <a href={getNext(card)} class="arrow" title="View next card">{">"}</a>
    </div>
</div>

<style>
    .arrow
    {
        text-decoration: none;
        font-weight: bold;
        color: var(--background);
        transition: var(--transition);
    }

    .arrow:hover
    {
        opacity: 50%;;
    }

    .left,.right
    {
        min-width: 5rem;
        font-size: 5rem;
        cursor:pointer;
        text-align: center;
        transform: translate(0,10rem);
    }

    .center
    {
        width : max(20vw, 15vh);
    }

    .card-panel
    {
        margin:0;
        width : 100%;
        display: flex;
        flex-direction: row;
        flex-wrap: nowrap;
        justify-content: center;
    }

    @media (max-aspect-ratio: 1/1) 
    {
        .center
        {
            width : 70vw;
        }

        .left,.right
        {
            padding-top: 60%;
            font-size: 2rem;
            width : 15vw;
        }
    }
</style>