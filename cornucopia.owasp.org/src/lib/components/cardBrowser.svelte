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
        mappingData: Record<string, unknown>;
    }

    let { card, cards, mappingData }: Props = $props();
    let t = readTranslation();

    function getUrl(c: Card | undefined): string {
        if (!c) return '';
        return c.url + '/#card';
    }

    function goToNext(event: MouseEvent, thisCard: Card) {
        event.preventDefault();
        const nextCard = cards.get(thisCard.next);
        if (nextCard) goto(getUrl(nextCard));
    }

    function goToPrevious(event: MouseEvent, thisCard: Card) {
        event.preventDefault();
        const prevCard = cards.get(thisCard.prevous);
        if (prevCard) goto(getUrl(prevCard));
    }

    function checkKey(event: KeyboardEvent) {
        const KEYCODE_RIGHT = 39;
        const KEYCODE_LEFT = 37;
        const nextCard = cards.get(card.next);
        const prevCard = cards.get(card.prevous);
        if (event.keyCode == KEYCODE_RIGHT && nextCard) goto(getUrl(nextCard));
        if (event.keyCode == KEYCODE_LEFT && prevCard) goto(getUrl(prevCard));
    }

    onDestroy(() => { if (browser) document.onkeydown = null; });

    if (browser) document.onkeydown = checkKey;
</script>
<noscript>
    <div class="card-panel" id="card-face">
        <div class="left">
            <a href={cards.get(card.prevous)?.url + '/#card-face'} data-sveltekit-reload class="arrow" title="{$t('cards.cardBrowser.a1.title')}: {card.prevous}">&lt;</a>
        </div>
        <div class="center">
            <CardPreview bind:card={card} mapping={mappingData} style='browser-card-container'></CardPreview>
        </div>
        <div class="right">
            <a href={cards.get(card.next)?.url + '/#card-face'} data-sveltekit-reload class="arrow" title="{$t('cards.cardBrowser.a2.title')}: {card.next}">&gt;</a>
        </div>
    </div>
</noscript>
<div class="card-panel script" id="card">
    <div class="left">
        <a href={getUrl(cards.get(card.prevous))} onclick={(e)=>goToPrevious(e, card)} class="arrow" title="{$t('cards.cardBrowser.a1.title')}: {card.prevous}">&lt;</a>
    </div>
    <div class="center">
        <CardPreview bind:card={card} mapping={mappingData} style='browser-card-container'></CardPreview>
    </div>
    <div class="right">
        <a href={getUrl(cards.get(card.next))} onclick={(e)=>goToNext(e, card)} class="arrow" title="{$t('cards.cardBrowser.a2.title')}: {card.next}">&gt;</a>
    </div>
</div>
<style>
    .arrow
    {
        font-size: 5vw;
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
        width : max(24vw, 15vh);
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
            width : 60vw;
        }

        .left,.right
        {
            padding-top: 0%;
            width : 15vw;
        }
        .arrow {
            font-size: 5vw;
        }
    }
</style>