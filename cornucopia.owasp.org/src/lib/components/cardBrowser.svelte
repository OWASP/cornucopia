<script lang="ts">
    import CardPreview from "./cardPreview.svelte";
    import { onDestroy } from "svelte";
    import { browser } from "$app/environment";
    import type { Card } from "../../domain/card/card";
    import { goto } from "$app/navigation";
    import { resolve } from "$app/paths";
    import { readTranslation } from "$lib/stores/stores";
    interface Props {
        card: Card;
        cards: Map<string, Card>;
        mappingData: Record<string, unknown>;
    }

    let { card = $bindable(), cards, mappingData }: Props = $props();
    let t = readTranslation();
    let _nextCard = $derived(cards.get(card.next));
    let _previousCard = $derived(cards.get(card.prevous));
    function checkKey(event: KeyboardEvent) 
    {
        const KEYCODE_RIGHT = 39;
        const KEYCODE_LEFT = 37;
        if(event.keyCode == KEYCODE_RIGHT)
        {
            goto(resolve(getUrl(cards.get(card.next))));
            card = cards.get(card.next);
            _nextCard = cards.get(card.next);
            _previousCard = cards.get(card.prevous);
        }   

        if(event.keyCode == KEYCODE_LEFT)
        {
            goto(resolve(getUrl(cards.get(card.prevous))));
            card = cards.get(card.prevous);
            _nextCard = cards.get(card.next);
            _previousCard = cards.get(card.prevous);
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
        _nextCard = cards.get(card.next);
        _previousCard = cards.get(card.prevous);
        goto(resolve(getUrl(card)));
    }

    function goToPrevious(thisCard: Card)
    {
        card = cards.get(thisCard.prevous);
        _previousCard = cards.get(card.prevous);
        goto(resolve(getUrl(card)));
    }

    if(browser)
        document.onkeydown = checkKey;
</script>
<noscript>
    <div class="card-panel" id="card-face">
        <div class="left">
            <a
                href={resolve(cards.get(card.prevous)?.url + '/#card-face')}
                data-sveltekit-reload
                class="arrow"
                title="{$t('cards.cardBrowser.a1.title')}: {card.prevous}"
            >&lt;</a>
        </div>
        <div class="center">
            <CardPreview bind:card={card} mapping={mappingData} style='browser-card-container'></CardPreview>
        </div>
        <div class="right">
            <a
                href={resolve(cards.get(card.next)?.url + '/#card-face')}
                data-sveltekit-reload
                class="arrow"
                title="{$t('cards.cardBrowser.a2.title')}: {card.next}"
            >&gt;</a>
        </div>
    </div>
</noscript>
<div class="card-panel script" id="card">
    <div class="left">
        <a href={resolve(getUrl(card))} onclick={()=>goToPrevious(card)} class="arrow" title="{$t('cards.cardBrowser.a1.title')}: {card.prevous}">&lt;</a>
    </div>
    <div class="center">
        <CardPreview bind:card={card} mapping={mappingData} style='browser-card-container'></CardPreview>
    </div>
    <div class="right">
        <a href={resolve(getUrl(card))} onclick={()=>goToNext(card)} class="arrow" title="{$t('cards.cardBrowser.a2.title')}: {card.next}">&gt;</a>
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





