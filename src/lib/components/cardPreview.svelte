<script lang="ts">
    import type { Card } from "../../domain/card/card";
    import { cardColor } from "../../domain/card/cardColor";
    import { CardController } from "../../domain/card/cardController";
    export let cardData;
    export let card : Card = {} as Card;
    export let mapping : any;

    function getSuitColor(suit : string)
    {
        return cardColor.get(suit) ?? "black";
    }
</script>

<div class="card-render">
    <div class="left" style="background-color:{getSuitColor(card.suit)}">
        <h1 class="property-card-suit">{card?.suitName || 'EXPLANATION'}</h1>
    </div>
    <div class="right">
        
        {#if mapping}
        <h1 style="color:{getSuitColor(card.suit)}" class="property-card-number">{mapping?.value ?? ""}</h1>
        <p class="property-card-description">{(new CardController(cardData)).getCardDescription(card.suit,card.card) ?? "?"}</p>
        <p class="mapping-title">OWASP SCP</p>
        <p class="mapping-value">{mapping.owasp_scp || '-'}</p>
        <p class="mapping-title">OWASP ASVS</p>
        <p class="mapping-value">{mapping.owasp_asvs || '-'}</p>
        <p class="mapping-title">OWASP AppSensor</p>
        <p class="mapping-value">{mapping.owasp_appsensor || '-'}</p>
        <p class="mapping-title">CAPEC</p>
        <p class="mapping-value">{mapping.owasp_capec || '-'}</p>        
        <p class="mapping-title">SAFECODE</p>
        <p class="mapping-value">{mapping.safecode || '-'}</p>
        {:else if card.card == 'CORNUCOPIA' }
        <h1 style="color:{getSuitColor(card.suit)}" class="property-card-number">{card.cardName}</h1>
        <p class="property-card-description">{card.summary}</p>
        {:else if card.suitName == 'WILD CARD' }
        <h1 style="color:{getSuitColor(card.suit)}" class="property-card-number">Joker</h1>
        <p class="property-card-description">{(new CardController(cardData)).getCardDescription(card.suit,card.card)}</p>
        {:else if mapping?.value == 'A' }
        <h1 style="color:{getSuitColor(card.suit)}" class="property-card-number">A</h1>
        <p class="property-card-description">{(new CardController(cardData)).getCardDescription(card.suit,card.card)}</p>
        {:else}
        <h1 style="color:{getSuitColor(card.suit)}" class="property-card-number">{card?.cardName ?? "?"}</h1>
        <p class="property-card-description">{(new CardController(cardData)).getCardDescription(card.suit,card.card) ?? "?"}</p>
        {/if}
    </div>
</div>

<style>
    .mapping-title, .mapping-value
    {
        font-size: .5rem;
        margin:0;
        margin-left: .25rem;
        margin-right: .25rem;
    }

    .mapping-title
    {
        font-weight: bold;
    }

    .mapping-value
    {
        border-bottom: 1px rgb(192, 192, 192) solid;
    }

    
    .property-card-suit
    {
        transform: rotate(90deg);
        text-orientation: mixed;
        font-size: 1rem;
        padding-top: .70rem;
        font-weight: bold;
        padding-left: 1rem;
        width: 100%;
        white-space: nowrap;
        color:white;
    }


    .property-card-description
    {
        font-size: .65rem;
        padding: .25rem;
    }
    .property-card-number
    {
        margin:0;
        text-align: right;
        padding-right: .5rem;
        font-weight: bold;
        font-size: 2rem;
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

    .card-render:hover
    {
        filter: brightness(105%);
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