<script lang="ts">
    import type { Component } from "svelte";
    import type { Card } from "../../domain/card/card";
    import { cardColor } from "../../domain/card/cardColor";
    import MobileAppCardMapping from "./mobileAppCardMapping.svelte";
    import CompanionCardMapping from "./companionCardMapping.svelte";
    import EopCardMapping from "./eopCardMapping.svelte";

    const mappingComponents: Record<string, Component<any>> = {
        mobileapp: MobileAppCardMapping,
        companion: CompanionCardMapping,
        eop: EopCardMapping
    };

    interface Props {
        card?: Card;
        mapping: Record<string, unknown>;
        style?: string;
    }

    let { card = $bindable(), mapping, style = '' }: Props = $props();
    let previewStyle = $derived(style ? ' ' + style : '');
    let MappingComponent = $derived(mappingComponents[card?.edition ?? '']);

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

    function getRoyalTextColor (suit: string, id: string, value: string) {
        if (!cardColor?.get(suit)) return '';
        if (id == 'WC' || ['J', 'Q', 'K'].includes(value)) return 'royal-white-text';
    }

    function getTextColor(suit : string, id: string)
    {
        if (['CRM', 'CM', 'WC'].includes(id)) suit = suit + '-mobile';
        return cardColor?.get(suit) ?? "default";
    }

    function getLeftRibbonClass(suit: string, id: string, value: string)
    {
        const base = getSuitColor(suit, id);
        if (!base) return base;
        if (['J', 'Q', 'K'].includes(value)) return base + ' left-royal';
        return base;
    }

    // handles the conversion of the value for the EoP cards between the copi and cornucopia codebases
    function eopValue(value: string)
    {
        return value === 'X' ? '10' : value;
    }
</script>

{#if card?.edition === 'eop'}
<div class="card-render eop {card?.suit} n{eopValue(card?.value)}">
    <div class="left-value">{eopValue(card?.value)}</div>
    <div class="main-content">
        <p class="category">{card?.suitName}</p>
        <p class="description">{card?.desc}</p>
    </div>
</div>
{:else}
<div class="card-render">
    <div class="left {getLeftRibbonClass(card?.suit, card?.suitId, card?.value)}">
        <span class="property-card-suit{previewStyle}">{card?.suitName}</span>
    </div>
    <div class="right {getRoyalSuitColor(card?.suit, card?.suitId, card?.value)}">
        
        {#if mapping}
        <span class="property-card-number{previewStyle} {getTextColor(card?.suit, card?.suitId)}-text {getRoyalTextColor(card?.suit, card?.suitId, card?.value)}">{card?.card ?? card?.value}</span>
        <p class="property-card-description{previewStyle}">{card?.desc}</p>
            {#if MappingComponent}
                <svelte:component this={MappingComponent} {mapping} {style} />
            {/if}
        {:else if card?.suitName == 'WILD CARD'}
        <span class="property-card-number {getSuitColor(card.suit, card?.suitId)}">Joker</span>
        <p class="property-card-description{previewStyle}">{card.desc}</p>
        {:else}
        <span class="property-card-number {getSuitColor(card?.suit, card?.suitId)}">{card?.value}</span>
        <p class="property-card-description{previewStyle}">{card?.desc}</p>
        {/if}
    </div>
</div>
{/if}

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
        font-size: 1.2vw;
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
    
    .left.agentic-ai {
        background: linear-gradient(180deg, #3b2c42, #3b2c4280);
    }
    .left.automated-threats {
        background: linear-gradient(180deg, #d56859, #d5685980);
    }
    .left.cloud {
        background: linear-gradient(180deg, #D289B8, #D289B880);
    }
    .left.devops {
        background: linear-gradient(180deg, #a87441, #a8744180);
    }
    .left.frontend {
        background: linear-gradient(180deg, #806A62, #806A6280);
    }
    .left.large-language-models {
        background: linear-gradient(180deg, #a13763, #a1376380);
    }
    .social-engineering {
        background-color: #dbdbdb;
    }

    .agentic-ai-text {
        color: #3b2c42;
    }
    .automated-threats-text {
        color: #d56859;
    }
    .cloud-text {
        color: #d289b8;
    }
    .devops-text {
        color: #a87441;
    }
    .frontend-text {
        color: #806A62;
    }
    .large-language-models-text {
        color: #a13763;
    }
    .social-engineering-text {
        color: #dbdbdb;
    }

    .agentic-ai-royal {
        background-color: #3b2c4280;
    }
    .automated-threats-royal {
        background-color: #d5685980;
    }
    .cloud-royal {
        background-color: #D289B880;
    }
    .devops-royal {
        background-color: #a8744180;
    }
    .frontend-royal {
        background-color: #806A6280;
    }
    .large-language-models-royal {
        background-color: #a1376380;
    }
    .social-engineering-royal {
        background-color: #e8e8e8;
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
    .royal-black-text {
        color: black;
    }
    .royal-white-text {
        color: white;
    }

    @media (max-width: 1024px)
    {
        .card-render
        {
           border-radius: 2.62vw;
        }

        .property-card-description.browser-card-container
        {
            font-size: 2.8vw;
            padding: .25rem;
            line-height: 1.25;
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

    /* EoP card styles imported from copi.owasp.org/assets/css/cards.scss (.card and .card.eop) */
    .card-render.eop {
      width: clamp(240px, 24vw, 320px);
      height: clamp(351px, 35.1vw, 469px);
      border-radius: clamp(12px, 1.5vw, 16px);
    }

    .card-render.eop .left-value {
      box-sizing: border-box; /* fixes the double height issue of card number box */
      flex: none;
      position: relative;
      top: clamp(36px, 3.6vw, 48px);
      height: clamp(72px, 7.2vw, 96px);
      width: clamp(55px, 5.5vw, 74px);
      background: grey;
      padding: clamp(28px, 2.8vw, 37px) 0;
      border-top-right-radius: clamp(12px, 1.2vw, 16px);
      border-bottom-right-radius: clamp(12px, 1.2vw, 16px);
      color: #fff;
      text-transform: uppercase;
      font-family: "Segoe Condensed";
      font-size: clamp(41px, 4.1vw, 55px);
      font-weight: 600;
      text-align: center;
      line-height: clamp(14px, 1.4vw, 22px);
    }

    .card-render.eop .main-content {
      overflow: hidden;
      flex: auto;
      padding: clamp(13px, 1.3vw, 18px) clamp(12px, 1.2vw, 16px);
    }

    .card-render.eop .main-content .category {
      margin: clamp(38px, 3.8vw, 51px) 0 0 0;
      font-family: "Segoe Light";
      font-size: clamp(22px, 2.2vw, 29px);
      font-weight: 300;
    }

    .card-render.eop .main-content .description {
      font-family: "Segoe";
      font-size: clamp(12px, 1.2vw, 16px);
      padding-right: 0px;
      line-height: 1.3;
    }

    .card-render.eop.spoofing .left-value {
      background: rgb(117, 35, 26);
    }

    .card-render.eop.spoofing.nJ, .card-render.eop.spoofing.nQ, .card-render.eop.spoofing.nK {
      background: rgb(178, 25, 74);
    }

    .card-render.eop.spoofing.nJ .main-content, .card-render.eop.spoofing.nQ .main-content, .card-render.eop.spoofing.nK .main-content {
      color: #fff;
    }

    .card-render.eop.spoofing.n2 {
      background: no-repeat top/100% url("/images/eop-cards/spoofing-2.png") #fff;
    }

    .card-render.eop.spoofing.n3 {
      background: no-repeat top/100% url("/images/eop-cards/spoofing-3.png") #fff;
    }

    .card-render.eop.spoofing.n4 {
      background: no-repeat bottom/100% url("/images/eop-cards/spoofing-4.png") #fff;
    }

    .card-render.eop.spoofing.n5 {
      background: no-repeat top/100% url("/images/eop-cards/spoofing-5.png") #fff;
    }

    .card-render.eop.spoofing.n6 {
      background: no-repeat bottom/100% url("/images/eop-cards/spoofing-6.png") #fff;
    }

    .card-render.eop.spoofing.n7 {
      background: no-repeat center/100% url("/images/eop-cards/spoofing-7.png") #fff;
    }

    .card-render.eop.spoofing.n8 {
      background: no-repeat top/100% url("/images/eop-cards/spoofing-8.png") #fff;
    }

    .card-render.eop.spoofing.n9 {
      background: no-repeat center/100% url("/images/eop-cards/spoofing-9.png") #fff;
    }

    .card-render.eop.spoofing.n10 {
      background: no-repeat top/100% url("/images/eop-cards/spoofing-10.png") #fff;
    }

    .card-render.eop.spoofing.nJ {
      background: no-repeat center/100% url("/images/eop-cards/spoofing-j.png") #fff;
    }

    .card-render.eop.spoofing.nQ {
      background: no-repeat center/100% url("/images/eop-cards/spoofing-q.png") #fff;
    }

    .card-render.eop.spoofing.nK {
      background: no-repeat center/100% url("/images/eop-cards/spoofing-k.png") #fff;
    }

    .card-render.eop.spoofing.nA {
      background: no-repeat bottom/100% url("/images/eop-cards/spoofing-a.png") #fff;
    }

    .card-render.eop.spoofing.nJ, .card-render.eop.spoofing.nQ, .card-render.eop.spoofing.nK, .card-render.eop.spoofing.nA, .card-render.eop.spoofing.n2, .card-render.eop.spoofing.n3, .card-render.eop.spoofing.n4, .card-render.eop.spoofing.n5, .card-render.eop.spoofing.n6, .card-render.eop.spoofing.n7, .card-render.eop.spoofing.n8, .card-render.eop.spoofing.n9, .card-render.eop.spoofing.n10 {
      background-size: cover;
    }

    .card-render.eop.tampering .left-value {
      background: rgb(2, 113, 55);
    }

    .card-render.eop.tampering.nJ, .card-render.eop.tampering.nQ, .card-render.eop.tampering.nK {
      background: rgb(116, 187, 99);
    }

    .card-render.eop.tampering.nJ .main-content, .card-render.eop.tampering.nQ .main-content, .card-render.eop.tampering.nK .main-content {
      color: #fff;
    }

    .card-render.eop.tampering.n2 {
      background: no-repeat top/100% url("/images/eop-cards/tampering-2.png") #fff;
    }

    .card-render.eop.tampering.n3 {
      background: no-repeat top/100% url("/images/eop-cards/tampering-3.png") #fff;
    }

    .card-render.eop.tampering.n4 {
      background: no-repeat bottom/100% url("/images/eop-cards/tampering-4.png") #fff;
    }

    .card-render.eop.tampering.n5 {
      background: no-repeat top/100% url("/images/eop-cards/tampering-5.png") #fff;
    }

    .card-render.eop.tampering.n6 {
      background: no-repeat bottom/100% url("/images/eop-cards/tampering-6.png") #fff;
    }

    .card-render.eop.tampering.n7 {
      background: no-repeat center/100% url("/images/eop-cards/tampering-7.png") #fff;
    }

    .card-render.eop.tampering.n8 {
      background: no-repeat top/100% url("/images/eop-cards/tampering-8.png") #fff;
    }

    .card-render.eop.tampering.n9 {
      background: no-repeat center/100% url("/images/eop-cards/tampering-9.png") #fff;
    }

    .card-render.eop.tampering.n10 {
      background: no-repeat top/100% url("/images/eop-cards/tampering-10.png") #fff;
    }

    .card-render.eop.tampering.nJ {
      background: no-repeat top/100% url("/images/eop-cards/tampering-j.png") #fff;
    }

    .card-render.eop.tampering.nQ {
      background: no-repeat top/100% url("/images/eop-cards/tampering-q.png") #fff;
    }

    .card-render.eop.tampering.nK {
      background: no-repeat center/100% url("/images/eop-cards/tampering-k.png") #fff;
    }

    .card-render.eop.tampering.nA {
      background: no-repeat bottom/100% url("/images/eop-cards/tampering-a.png") #fff;
    }

    .card-render.eop.tampering.nJ, .card-render.eop.tampering.nQ, .card-render.eop.tampering.nK, .card-render.eop.tampering.nA, .card-render.eop.tampering.n2, .card-render.eop.tampering.n3, .card-render.eop.tampering.n4, .card-render.eop.tampering.n5, .card-render.eop.tampering.n6, .card-render.eop.tampering.n7, .card-render.eop.tampering.n8, .card-render.eop.tampering.n9, .card-render.eop.tampering.n10 {
      background-size: cover;
    }

    .card-render.eop.repudiation .left-value {
      background: rgb(117, 35, 26);
    }

    .card-render.eop.repudiation.nJ, .card-render.eop.repudiation.nQ, .card-render.eop.repudiation.nK {
      background: rgb(229, 114, 63);
    }

    .card-render.eop.repudiation.nJ .main-content, .card-render.eop.repudiation.nQ .main-content, .card-render.eop.repudiation.nK .main-content {
      color: #fff;
    }

    .card-render.eop.repudiation.n2 {
      background: no-repeat top/100% url("/images/eop-cards/repudiation-2.png") #fff;
    }

    .card-render.eop.repudiation.n3 {
      background: no-repeat top/100% url("/images/eop-cards/repudiation-3.png") #fff;
    }

    .card-render.eop.repudiation.n4 {
      background: no-repeat bottom/100% url("/images/eop-cards/repudiation-4.png") #fff;
    }

    .card-render.eop.repudiation.n5 {
      background: no-repeat top/100% url("/images/eop-cards/repudiation-5.png") #fff;
    }

    .card-render.eop.repudiation.n6 {
      background: no-repeat bottom/100% url("/images/eop-cards/repudiation-6.png") #fff;
    }

    .card-render.eop.repudiation.n7 {
      background: no-repeat center/100% url("/images/eop-cards/repudiation-7.png") #fff;
    }

    .card-render.eop.repudiation.n8 {
      background: no-repeat top/100% url("/images/eop-cards/repudiation-8.png") #fff;
    }

    .card-render.eop.repudiation.n9 {
      background: no-repeat center/100% url("/images/eop-cards/repudiation-9.png") #fff;
    }

    .card-render.eop.repudiation.n10 {
      background: no-repeat top/100% url("/images/eop-cards/repudiation-10.png") #fff;
    }

    .card-render.eop.repudiation.nJ {
      background: no-repeat center/100% url("/images/eop-cards/repudiation-j.png") #fff;
    }

    .card-render.eop.repudiation.nQ {
      background: no-repeat center/100% url("/images/eop-cards/repudiation-q.png") #fff;
    }

    .card-render.eop.repudiation.nK {
      background: no-repeat bottom/100% url("/images/eop-cards/repudiation-k.png") #fff;
    }

    .card-render.eop.repudiation.nA {
      background: no-repeat bottom/100% url("/images/eop-cards/repudiation-a.png") #fff;
    }

    .card-render.eop.repudiation.nJ, .card-render.eop.repudiation.nQ, .card-render.eop.repudiation.nK, .card-render.eop.repudiation.nA, .card-render.eop.repudiation.n2, .card-render.eop.repudiation.n3, .card-render.eop.repudiation.n4, .card-render.eop.repudiation.n5, .card-render.eop.repudiation.n6, .card-render.eop.repudiation.n7, .card-render.eop.repudiation.n8, .card-render.eop.repudiation.n9, .card-render.eop.repudiation.n10 {
      background-size: cover;
    }

    .card-render.eop.information-disclosure .left-value {
      background: rgb(255, 240, 39);
    }

    .card-render.eop.information-disclosure.nJ, .card-render.eop.information-disclosure.nQ, .card-render.eop.information-disclosure.nK {
      background: rgb(0, 159, 156);
    }

    .card-render.eop.information-disclosure.nJ .main-content, .card-render.eop.information-disclosure.nQ .main-content, .card-render.eop.information-disclosure.nK .main-content {
      color: #fff;
    }

    .card-render.eop.information-disclosure.n2 {
      background: no-repeat top/100% url("/images/eop-cards/information-disclosure-2.png") #fff;
    }

    .card-render.eop.information-disclosure.n3 {
      background: no-repeat top/100% url("/images/eop-cards/information-disclosure-3.png") #fff;
    }

    .card-render.eop.information-disclosure.n4 {
      background: no-repeat bottom/100% url("/images/eop-cards/information-disclosure-4.png") #fff;
    }

    .card-render.eop.information-disclosure.n5 {
      background: no-repeat top/100% url("/images/eop-cards/information-disclosure-5.png") #fff;
    }

    .card-render.eop.information-disclosure.n6 {
      background: no-repeat bottom/100% url("/images/eop-cards/information-disclosure-6.png") #fff;
    }

    .card-render.eop.information-disclosure.n7 {
      background: no-repeat top/100% url("/images/eop-cards/information-disclosure-7.png") #fff;
    }

    .card-render.eop.information-disclosure.n8 {
      background: no-repeat top 15px left/100% url("/images/eop-cards/information-disclosure-8.png") #fff;
    }

    .card-render.eop.information-disclosure.n9 {
      background: no-repeat center/100% url("/images/eop-cards/information-disclosure-9.png") #fff;
    }

    .card-render.eop.information-disclosure.n10 {
      background: no-repeat top 28px left/100% url("/images/eop-cards/information-disclosure-10.png") #fff;
    }

    .card-render.eop.information-disclosure.nJ {
      background: no-repeat center/100% url("/images/eop-cards/information-disclosure-j.png") #fff;
    }

    .card-render.eop.information-disclosure.nQ {
      background: no-repeat top left/100% url("/images/eop-cards/information-disclosure-q.png") #fff;
    }

    .card-render.eop.information-disclosure.nK {
      background: no-repeat top 9px left/100% url("/images/eop-cards/information-disclosure-k.png") #fff;
    }

    .card-render.eop.information-disclosure.nA {
      background: no-repeat bottom/100% url("/images/eop-cards/information-disclosure-a.png") #fff;
    }

    .card-render.eop.information-disclosure.nJ, .card-render.eop.information-disclosure.nQ, .card-render.eop.information-disclosure.nK, .card-render.eop.information-disclosure.nA, .card-render.eop.information-disclosure.n2, .card-render.eop.information-disclosure.n3, .card-render.eop.information-disclosure.n4, .card-render.eop.information-disclosure.n5, .card-render.eop.information-disclosure.n6, .card-render.eop.information-disclosure.n7, .card-render.eop.information-disclosure.n8, .card-render.eop.information-disclosure.n9, .card-render.eop.information-disclosure.n10 {
      background-size: cover;
    }

    .card-render.eop.denial-of-service .left-value {
      background: rgb(26, 25, 25);
    }

    .card-render.eop.denial-of-service.nJ, .card-render.eop.denial-of-service.nQ, .card-render.eop.denial-of-service.nK {
      background: rgb(102, 102, 101);
    }

    .card-render.eop.denial-of-service.nJ .main-content, .card-render.eop.denial-of-service.nQ .main-content, .card-render.eop.denial-of-service.nK .main-content {
      color: #fff;
    }

    .card-render.eop.denial-of-service.n2 {
      background: no-repeat top/100% url("/images/eop-cards/denial-of-service-2.png") #fff;
    }

    .card-render.eop.denial-of-service.n3 {
      background: no-repeat top/100% url("/images/eop-cards/denial-of-service-3.png") #fff;
    }

    .card-render.eop.denial-of-service.n4 {
      background: no-repeat bottom/100% url("/images/eop-cards/denial-of-service-4.png") #fff;
    }

    .card-render.eop.denial-of-service.n5 {
      background: no-repeat top/100% url("/images/eop-cards/denial-of-service-5.png") #fff;
    }

    .card-render.eop.denial-of-service.n6 {
      background: no-repeat bottom/100% url("/images/eop-cards/denial-of-service-6.png") #fff;
    }

    .card-render.eop.denial-of-service.n7 {
      background: no-repeat center/100% url("/images/eop-cards/denial-of-service-7.png") #fff;
    }

    .card-render.eop.denial-of-service.n8 {
      background: no-repeat top/100% url("/images/eop-cards/denial-of-service-8.png") #fff;
    }

    .card-render.eop.denial-of-service.n9 {
      background: no-repeat top -15px left/100% url("/images/eop-cards/denial-of-service-9.png") #fff;
    }

    .card-render.eop.denial-of-service.n10 {
      background: no-repeat top 2px left/100% url("/images/eop-cards/denial-of-service-10.png") #fff;
    }

    .card-render.eop.denial-of-service.nJ {
      background: no-repeat center/100% url("/images/eop-cards/denial-of-service-j.png") #fff;
    }

    .card-render.eop.denial-of-service.nQ {
      background: no-repeat top -10px left/100% url("/images/eop-cards/denial-of-service-q.png") #fff;
    }

    .card-render.eop.denial-of-service.nK {
      background: no-repeat top/100% url("/images/eop-cards/denial-of-service-k.png") #fff;
    }

    .card-render.eop.denial-of-service.nA {
      background: no-repeat bottom/100% url("/images/eop-cards/denial-of-service-a.png") #fff;
    }

    .card-render.eop.denial-of-service.nJ, .card-render.eop.denial-of-service.nQ, .card-render.eop.denial-of-service.nK, .card-render.eop.denial-of-service.nA, .card-render.eop.denial-of-service.n2, .card-render.eop.denial-of-service.n3, .card-render.eop.denial-of-service.n4, .card-render.eop.denial-of-service.n5, .card-render.eop.denial-of-service.n6, .card-render.eop.denial-of-service.n7, .card-render.eop.denial-of-service.n8, .card-render.eop.denial-of-service.n9, .card-render.eop.denial-of-service.n10 {
      background-size: cover;
    }

    .card-render.eop.elevation-of-privilege .left-value {
      background: rgb(229, 114, 63);
    }

    .card-render.eop.elevation-of-privilege.nJ, .card-render.eop.elevation-of-privilege.nQ, .card-render.eop.elevation-of-privilege.nK {
      background: rgb(69, 139, 189);
    }

    .card-render.eop.elevation-of-privilege.nJ .main-content, .card-render.eop.elevation-of-privilege.nQ .main-content, .card-render.eop.elevation-of-privilege.nK .main-content {
      color: #fff;
    }

    .card-render.eop.elevation-of-privilege.n2 {
      background: no-repeat top/100% url("/images/eop-cards/elevation-of-privilege-2.png") #fff;
    }

    .card-render.eop.elevation-of-privilege.n3 {
      background: no-repeat top/100% url("/images/eop-cards/elevation-of-privilege-3.png") #fff;
    }

    .card-render.eop.elevation-of-privilege.n4 {
      background: no-repeat top/100% url("/images/eop-cards/elevation-of-privilege-4.png") #fff;
    }

    .card-render.eop.elevation-of-privilege.n5 {
      background: no-repeat top/100% url("/images/eop-cards/elevation-of-privilege-5.png") #fff;
    }

    .card-render.eop.elevation-of-privilege.n6 {
      background: no-repeat bottom/100% url("/images/eop-cards/elevation-of-privilege-6.png") #fff;
    }

    .card-render.eop.elevation-of-privilege.n7 {
      background: no-repeat center/100% url("/images/eop-cards/elevation-of-privilege-7.png") #fff;
    }

    .card-render.eop.elevation-of-privilege.n8 {
      background: no-repeat top 15px left/100% url("/images/eop-cards/elevation-of-privilege-8.png") #fff;
    }

    .card-render.eop.elevation-of-privilege.n9 {
      background: no-repeat top/100% url("/images/eop-cards/elevation-of-privilege-9.png") #fff;
    }

    .card-render.eop.elevation-of-privilege.n10 {
      background: no-repeat top 30px left/100% url("/images/eop-cards/elevation-of-privilege-10.png") #fff;
    }

    .card-render.eop.elevation-of-privilege.nJ {
      background: no-repeat center/100% url("/images/eop-cards/elevation-of-privilege-j.png") #fff;
    }

    .card-render.eop.elevation-of-privilege.nQ {
      background: no-repeat top -9px left/100% url("/images/eop-cards/elevation-of-privilege-q.png") #fff;
    }

    .card-render.eop.elevation-of-privilege.nK {
      background: no-repeat top/100% url("/images/eop-cards/elevation-of-privilege-k.png") #fff;
    }

    .card-render.eop.elevation-of-privilege.nA {
      background: no-repeat bottom/100% url("/images/eop-cards/elevation-of-privilege-a.png") #fff;
    }

    .card-render.eop.elevation-of-privilege.nJ, .card-render.eop.elevation-of-privilege.nQ, .card-render.eop.elevation-of-privilege.nK, .card-render.eop.elevation-of-privilege.nA, .card-render.eop.elevation-of-privilege.n2, .card-render.eop.elevation-of-privilege.n3, .card-render.eop.elevation-of-privilege.n4, .card-render.eop.elevation-of-privilege.n5, .card-render.eop.elevation-of-privilege.n6, .card-render.eop.elevation-of-privilege.n7, .card-render.eop.elevation-of-privilege.n8, .card-render.eop.elevation-of-privilege.n9, .card-render.eop.elevation-of-privilege.n10 {
      background-size: cover;
    }
</style>

