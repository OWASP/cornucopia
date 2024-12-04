<script lang="ts">
    import type { Card } from "../../domain/card/card";
    import { cardColor } from "../../domain/card/cardColor";
    import MobileAppCardMapping from "./mobileAppCardMapping.svelte";
    import WebAppCardMapping from "./webAppCardMapping.svelte";
    export let card : Card = {} as Card;
    export let mapping : any;

    function getSuitColor(suit : string)
    {
        return cardColor?.get(suit) ?? "black";
    }
</script>

<div class="card-render">
    <div class="left" style="background-color:{getSuitColor(card.suit)}">
        <h1 class="property-card-suit">{card?.suitName}</h1>
    </div>
    <div class="right">
        
        {#if mapping}
        <h1 style="color:{getSuitColor(card.suit)}" class="property-card-number">{card?.card ?? card?.value}</h1>
        <p class="property-card-description">{card.desc}</p>
            {#if card.edition == 'webapp' && card.value != 'A' && card.value != 'B'}
                <WebAppCardMapping {mapping}></WebAppCardMapping>
            {/if}
            {#if card.edition == 'mobileapp' && card.value != 'A' && card.value != 'B'}
                <MobileAppCardMapping {mapping}></MobileAppCardMapping>
            {/if}
        {:else if card.suitName == 'WILD CARD' }
        <h1 style="color:{getSuitColor(card.suit)}" class="property-card-number">Joker</h1>
        <p class="property-card-description">{card.desc}</p>
        {:else}
        <h1 style="color:{getSuitColor(card.suit)}" class="property-card-number">{card?.value}</h1>
        <p class="property-card-description">{card.desc}</p>
        {/if}
    </div>
</div>

<style>
    .property-card-suit
    {
        transform: rotate(90deg);
        text-orientation: mixed;
        font-size: max(1.3vw, 3vh);
        padding-top: .70rem;
        font-weight: bold;
        padding-left: 1rem;
        width: 100%;
        white-space: nowrap;
        color:white;
    }


    .property-card-description
    {
        font-size: max(.8vw, 1.5vh);
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
        margin-top: 2rem;
        border: 1px rgb(197, 197, 197) solid;
        box-shadow: rgba(50, 50, 93, 0.25) 0px 13px 27px -5px, rgba(0, 0, 0, 0.3) 0px 8px 16px -8px;
        background-color: white;
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