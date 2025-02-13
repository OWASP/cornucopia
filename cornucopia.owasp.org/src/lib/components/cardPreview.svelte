<script lang="ts">
    import type { Card } from "../../domain/card/card";
    import { cardColor } from "../../domain/card/cardColor";
    import MobileAppCardMapping from "./mobileAppCardMapping.svelte";
    import WebAppCardMapping from "./webAppCardMapping.svelte";
    
    interface Props {
        card?: Card;
        mapping: any;
        style?: string;
    }

    let { card = $bindable(), mapping, style = '' }: Props = $props();
    let previewStyle = $state('');

    if (style) {
        previewStyle = ' ' + style;
    }

    function getSuitColor(suit : string, id: string)
    {
        if (['CRM', 'CM', 'WC'].includes(id)) suit = suit + '-mobile';
        return cardColor?.get(suit) ?? "";
    }

    function getRoyalSuitColor(suit: string, id: string, value: string)
    {
        if (!cardColor?.get(suit)) return 'white';
        if (id != 'WC' && !['J', 'Q', 'K'].includes(value)) return 'white';
        suit = cardColor?.get(suit) + '-royal';
        if (['CRM', 'CM', 'WC'].includes(id)) suit = suit + '-mobile';
        return suit;
    }

    function getTextColor(suit : string, id: string)
    {
        if (['CRM', 'CM', 'WC'].includes(id)) suit = suit + '-mobile';
        return cardColor?.get(suit) ?? "default";
    }
</script>

<div class="card-render">
    <div class="left {getSuitColor(card?.suit, card?.suitId)}">
        <span class="property-card-suit{previewStyle}">{card?.suitName}</span>
    </div>
    <div class="right {getRoyalSuitColor(card?.suit, card?.suitId, card?.value)}">
        
        {#if mapping}
        <span class="property-card-number{previewStyle} {getTextColor(card?.suit, card?.suitId)}-text">{card?.card ?? card?.value}</span>
        <p class="property-card-description{previewStyle}">{card?.desc}</p>
            {#if card?.edition == 'webapp' && card?.value != 'A' && card?.value != 'B'}
                <WebAppCardMapping {mapping} {style}></WebAppCardMapping>
            {/if}
            {#if card?.edition == 'mobileapp' && card?.value != 'A' && card?.value != 'B'}
                <MobileAppCardMapping {mapping}  {style}></MobileAppCardMapping>
            {/if}
        {:else if card?.suitName == 'WILD CARD'}
        <h1 class="property-card-number {getSuitColor(card.suit, card?.suitId)}">Joker</h1>
        <p class="property-card-description{previewStyle}">{card.desc}</p>
        {:else}
        <h1 class="property-card-number {getSuitColor(card?.suit, card?.suitId)}">{card?.value}</h1>
        <p class="property-card-description{previewStyle}">{card?.desc}</p>
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
        padding-top: 1vw;
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

    .property-card-suit.preview-card-container
    {
        font-size: 1.8vw;
    }

    .property-card-description.preview-card-container
    {
        font-size: 1.3vw;
    }

    .property-card-number.preview-card-container
    {
        font-size: 5vw;
    }
    
    .property-card-suit.browser-card-container
    {
        font-size: 1.5vw;
    }

    .property-card-description.browser-card-container
    {
        font-size: 1vw;
    }

    .property-card-number.browser-card-container
    {
        font-size: 3vw;
    }

    .card-render
    {
        overflow: hidden;
        display: flex;
        width : 100%;
        aspect-ratio: 20/32;
        border-radius: 0.62vw;
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

    .authentication {
        background-color: #8FC4E8;
    }
    .authorization {
        background-color: #ECCE3E;
    }
    .data-validation-and-encoding {
        background-color: #B5B1AF;
    }
    .cornucopia {
        background-color: #526994;
    }
    .session-management {
        background-color: #B1D579;
    }
    .cryptography {
        background-color: #C3B2E3;
    }
    .wild-card {
        background-color: #FBB67C;
    }
    .wild-card-mobile {
        background: rgb(251,182,124);
        background: linear-gradient(180deg, rgba(251,182,124,1) 22%, rgba(255,230,209,1) 100%);
    }
    .platform-and-code {
        background: rgb(79,185,145);
        background: linear-gradient(180deg, rgba(79,185,145,1) 30%, rgba(95,172,211,1) 85%);
    }
    .authentication-and-authorization {
        background: rgb(240,156,44);
        background: linear-gradient(180deg, rgba(240,156,44,1) 20%, rgba(240,179,98,1) 77%);
    }
    .network-and-storage {
        background: rgb(223,92,141);
        background: linear-gradient(180deg, rgba(241,194,25,1) 0%, rgba(223,92,141,1) 85%);
    }
    .resilience {
        background: rgb(49,124,192);
        background: linear-gradient(180deg, rgba(49,124,192,1) 20%, rgba(79,138,192,1) 63%);
    }
    .cryptography-mobile {
        background: rgb(246,89,40);
        background: linear-gradient(180deg, rgba(246,89,40,1) 0%, rgba(246,135,101,1) 100%);
    }
    .cornucopia-mobile {
        background: rgb(10,58,94);
        background: linear-gradient(180deg, rgba(10,58,94,1) 22%, rgba(39,70,94,1) 74%);
    }

    .authentication-text {
        color: #8FC4E8;
    }
    .authorization-text {
        color: #ECCE3E;
    }
    .data-validation-and-encoding-text {
        color: #B5B1AF;
    }
    .cornucopia-text {
        color: #526994;
    }
    .session-management-text {
        color: #B1D579;
    }
    .cryptography-text {
        color: #C3B2E3;
    }
    .wild-card-text {
        color: #FBB67C;
    }
    .wild-card-mobile-text {
        color: rgb(251,182,124);
    }
    .platform-and-code-text {
        color: rgb(79,185,145);
    }
    .authentication-and-authorization-text {
        color: rgb(240,156,44);
    }
    .network-and-storage-text {
        color: rgba(241,194,25)
    }
    .resilience-text {
        color: rgb(49,124,192);
    }
    .cryptography-mobile-text {
        color: rgb(246,89,40);
    }
    .cornucopia-mobile-text {
        color: rgb(10,58,94);
    }

    .white {
        background-color: white;
    }

    .authentication-royal {
        background-color: #d3e4ed;
    }
    .authorization-royal {
        background-color: #eee6c6;
    }
    .data-validation-and-encoding-royal {
        background-color: #dfdfe0;
    }
    .cornucopia-royal {
        background-color: #ced8df;
    }
    .session-management-royal {
        background-color: #ddedd9;
    }
    .cryptography-royal {
        background-color: #dbd8eb;
    }
    .wild-card-royal {
        background-color: #fee9d8;
    }
    .wild-card-royal-mobile {
        background: rgb(255,230,209);
        background: linear-gradient(90deg, rgba(255,230,209,0.7) 0%, rgba(251,182,124,0.7) 100%);
    }
    .platform-and-code-royal {
        background: rgb(95,172,211);
        background: linear-gradient(90deg, rgba(95,172,211,0.5) 0%, rgba(79,185,145,0.5) 100%);
    }
    .authentication-and-authorization-royal {
        background: rgb(240,179,98);
        background: linear-gradient(90deg, rgba(240,179,98,0.5) 0%, rgba(240,156,44,0.5) 100%);
    }
    .network-and-storage-royal {
        background: rgb(223,92,141);
        background: linear-gradient(90deg, rgba(223,92,141,0.5) 0%, rgba(242,194,0,0.5) 100%);
    }
    .resilience-royal {
        background: rgb(79,138,192);
        background: linear-gradient(90deg, rgba(79,138,192,0.5) 0%, rgba(49,124,192,0.5) 100%);
    }
    .cryptography-royal-mobile {
        background: rgb(246,135,101);
        background: linear-gradient(90deg, rgba(246,135,101,0.5) 0%, rgba(246,89,40,0.5) 100%);
    }
    .cornucopia-royal-mobile {
        background: rgb(39,70,94);
        background: linear-gradient(90deg, rgba(39,70,94,0.2) 0%, rgba(10,58,94,0.2) 100%);
    }

    @media (max-aspect-ratio: 1.5/1)
    {
        .card-render
        {
           
        }

        .property-card-description.browser-card-container
        {
            font-size: 3.5vw;
            padding: .25rem;
        }

        .property-card-suit.browser-card-container
        {
            font-size: 3.5vw;
            padding-top: 8vw;
            padding-left: 8vw;

        }
        .property-card-number.browser-card-container
        {
            font-size: 10vw;
        }
    }
</style>