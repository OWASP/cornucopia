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

    function getSuitColor(suit : string)
    {
        return cardColor?.get(suit) ?? "";
    }

    function getTextColor(suit : string)
    {
        return cardColor?.get(suit) ?? "default";
    }
</script>

<div class="card-render">
    <div class="left {getSuitColor(card.suit)}">
        <span class="property-card-suit{previewStyle}">{card?.suitName}</span>
    </div>
    <div class="right">
        
        {#if mapping}
        <span class="property-card-number{previewStyle} {getTextColor(card.suit)}-text">{card?.card ?? card?.value}</span>
        <p class="property-card-description{previewStyle}">{card.desc}</p>
            {#if card.edition == 'webapp' && card.value != 'A' && card.value != 'B'}
                <WebAppCardMapping {mapping} {style}></WebAppCardMapping>
            {/if}
            {#if card.edition == 'mobileapp' && card.value != 'A' && card.value != 'B'}
                <MobileAppCardMapping {mapping}  {style}></MobileAppCardMapping>
            {/if}
        {:else if card.suitName == 'WILD CARD'}
        <h1 class="property-card-number {getSuitColor(card.suit)}">Joker</h1>
        <p class="property-card-description{previewStyle}">{card.desc}</p>
        {:else}
        <h1 class="property-card-number {getSuitColor(card.suit)}">{card?.value}</h1>
        <p class="property-card-description{previewStyle}">{card.desc}</p>
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
    .platform-and-code {
        background-color: #00FFBF;
    }
    .authentication-and-authorization {
        background-color: #FFD500;
    }
    .network-and-storage {
        background-color: #FF6600;
    }
    .resilience {
        background-color: #006EFF;
    }
    .cryptography-mobile {
        background-color: #006EFF;
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
    .platform-and-code-text {
        color: #00FFBF;
    }
    .authentication-and-authorization-text {
        color: #FFD500;
    }
    .network-and-storage-text {
        color: #FF6600;
    }
    .resilience-text {
        color: #006EFF;
    }
    .cryptography-mobile-text {
        color: #006EFF;
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