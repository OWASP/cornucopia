<script lang="ts">
    import type { Card } from "../../domain/card/card";
    import { cardColor } from "../../domain/card/cardColor";
    import MobileAppCardMapping from "./mobileAppCardMapping.svelte";
    import WebAppCardMapping from "./webAppCardMapping.svelte";
    export let card : Card = {} as Card;
    export let mapping : any;
    export let hero : string = '';
    let heroStyle = '';

    if (hero == 'yes') {
        heroStyle = ' hero-card-container';
    }

    function getSuitColor(suit : string)
    {
        return cardColor?.get(suit) ?? "black";
    }
</script>

<div class="card-render">
    <div class="left" style="background-color:{getSuitColor(card.suit)}">
        <span class="property-card-suit{heroStyle}">{card?.suitName}</span>
    </div>
    <div class="right">
        
        {#if mapping}
        <span style="color:{getSuitColor(card.suit)}" class="property-card-number">{card?.card ?? card?.value}</span>
        <p class="property-card-description{heroStyle}">{card.desc}</p>
            {#if card.edition == 'webapp' && card.value != 'A' && card.value != 'B'}
                <WebAppCardMapping {mapping} {hero}></WebAppCardMapping>
            {/if}
            {#if card.edition == 'mobileapp' && card.value != 'A' && card.value != 'B'}
                <MobileAppCardMapping {mapping}></MobileAppCardMapping>
            {/if}
        {:else if card.suitName == 'WILD CARD' }
        <h1 style="color:{getSuitColor(card.suit)}" class="property-card-number">Joker</h1>
        <p class="property-card-description{heroStyle}">{card.desc}</p>
        {:else}
        <h1 style="color:{getSuitColor(card.suit)}" class="property-card-number">{card?.value}</h1>
        <p class="property-card-description{heroStyle}">{card.desc}</p>
        {/if}
    </div>
</div>

<style>
    span
    {
        display: block;
        margin-top: .5rem;
    }
    .property-card-suit
    {
        transform: rotate(90deg);
        text-orientation: mixed;
        font-size: max(1.5vh, 1.8vw);
        padding-top: .70rem;
        font-weight: bold;
        padding-left: 1rem;
        width: 100%;
        white-space: nowrap;
        color:white;
    }


    .property-card-description
    {
        font-size: max(1.5vh, 0.9vw);
        padding: .25rem;
    }
    .property-card-number
    {
        margin:0;
        text-align: right;
        padding-right: .5rem;
        font-weight: bold;
        font-size: max(3vw,5vh);
    }
    .card-render
    {
        overflow: hidden;
        display: flex;
        width : 100%;
        aspect-ratio: 20/32;
        border-radius: 1.2rem;
        background-position: 50% 50%;
        background-size: 117%;
        transition: var(--transition);
        border: 1px rgb(197, 197, 197) solid;
        box-shadow: rgba(50, 50, 93, 0.25) 0px 13px 27px -5px, rgba(0, 0, 0, 0.3) 0px 8px 16px -8px;
        background-color: white;
    }
    p.hero-card-container
    {
        font-size: max(0.1vh, 0.6vw);
    }

    span.hero-card-container
    {
        font-size: max(1.3vh, 1.2vw);
    }

    .left
    {
        width: 15%;
        background: rgb(2,0,36);
        background: linear-gradient(0deg, rgba(0, 0, 0, 0.1) 0%, rgba(255,255,255,0.3) 100%);
    }

    .right
    {
        width: 85%;
    }
</style>