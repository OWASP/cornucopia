<script lang="ts">
    import { GetCardImageUrl } from "$lib/cards";
    import CardPreview from "./cardPreview.svelte";
    import { onDestroy } from "svelte";
    import { browser } from "$app/environment";
    import type { Card } from "../../domain/card/card";
    import { goto } from "$app/navigation";

    export let card : Card;
    export let cards : Card[];
  
    function checkKey(event : any) 
    {
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

    function getCurrentIndex(card : Card)
    {
        // cards are equal when both their suit and card value (e.g. authentication 4) are equal.
        return cards.map(card => card.suit + card.card).indexOf(card.suit + card.card);
    }


    function getPrevious(card : Card)
    {
        let index = getCurrentIndex(card);
        index -= 1;
        index = index % cards.length;
        if(index < 0)
            index = cards.length - 1;

        let previousCard = cards[index];
        return '/' + previousCard.suit + '/' + previousCard.card + '/#card';    
    }

    function getNext(card : Card)
    {
        let index = getCurrentIndex(card);
        index += 1;
        index = index % cards.length;
        let nextCard = cards[index];
        return '/' + nextCard.suit + '/' + nextCard.card + '/#card';
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
        <CardPreview url={GetCardImageUrl(card.suit,card.card)}></CardPreview>
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
        width : max(15vw, 15vh);
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