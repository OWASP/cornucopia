<script lang="ts">
    import CardPreview from "./cardPreview.svelte";
    import { onDestroy } from "svelte";
    import { browser } from "$app/environment";
    import type { Card } from "../../domain/card/card";
    import { goto } from "$app/navigation";
    import { readTranslation } from "$lib/stores/stores";
    interface Props {
        card: Card;
        cards: Map<string, Card>;
        mappingData: any;
    }

    let { card = $bindable(), cards, mappingData }: Props = $props();
    let t = readTranslation();
    let nextCard = cards.get(card.next);
    let previousCard = cards.get(card.prevous);
    function checkKey(event : any) 
    {
        const KEYCODE_RIGHT = 39;
        const KEYCODE_LEFT = 37;
        if(event.keyCode == KEYCODE_RIGHT)
        {
            goto(getUrl(cards.get(card.next)));
            card = cards.get(card.next);
            nextCard = cards.get(card.next);
            previousCard = cards.get(card.prevous);
        }   

        if(event.keyCode == KEYCODE_LEFT)
        {
            goto(getUrl(cards.get(card.prevous)));
            card = cards.get(card.prevous);
            nextCard = cards.get(card.next);
            previousCard = cards.get(card.prevous);
        }
    }

    function getUrl(card: Card)
    {
        return cards.get(card.id)?.url + '/#card';
    }

    onDestroy(()=> {if(browser)document.onkeydown = null})

    function goToNext(thisCard: Card)
    {
        card = cards.get(thisCard.next);
        nextCard = cards.get(card.next);
        previousCard = cards.get(card.prevous);
        goto(getUrl(card));
    }

    function goToPrevious(thisCard: Card)
    {
        card = cards.get(thisCard.prevous);
        nextCard = cards.get(thisCard.next);
        previousCard = cards.get(card.prevous);
        goto(getUrl(card));
    }

    if(browser)
        document.onkeydown = checkKey;
</script>
<noscript>
    <div class="card-panel" id="card-face">
        <div class="left">
            <a href={card.prevous + '/#card-face'} data-sveltekit-reload class="arrow" title="{$t('cards.cardBrowser.a1.title')}">{"<"}</a>
        </div>
        <div class="center">
            <CardPreview bind:card={card} mapping={mappingData} style='browser-card-container'></CardPreview>
        </div>
        <div class="right">
            <a href={card.next + '/#card-face'} data-sveltekit-reload class="arrow" title="{$t('cards.cardBrowser.a2.title')}">{">"}</a>
        </div>
    </div>
</noscript>
<div class="card-panel script" id="card">
    <div class="left">
        <a href={getUrl(card)} onclick={()=>goToPrevious(card)} class="arrow" title="{$t('cards.cardBrowser.a1.title')}">{"<"}</a>
    </div>
    <div class="center">
        <CardPreview bind:card={card} mapping={mappingData} style='browser-card-container'></CardPreview>
    </div>
    <div class="right">
        <a href={getUrl(card)} onclick={()=>goToNext(card)} class="arrow" title="{$t('cards.cardBrowser.a2.title')}">{">"}</a>
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
        opacity: 50%;
    }

    .left,.right
    {
        min-width: 5vw;
        font-size: 5vw;
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

    @media (max-aspect-ratio: 1.5/1) 
    {
        .center
        {
            width : 70vw;
        }

        .left,.right
        {
            padding-top: 60%;
            width : 15vw;
        }
    }
</style>