<script lang="ts">
    import CardPreview from "../cardPreview.svelte";
    import type { Suit } from "../../../domain/suit/suit";
    import type { Card } from "../../../domain/card/card";

    export let suits : Suit[];
    export let cardData : any;
    export let mapping : any;
    // Get a card from every suit
    let cards : Card[] = suits.map((suit) => suit.cards[0]).reverse();
    let mappingData : any[] = mapping.suits.map((suit: { cards: any[]; }) => suit.cards[0]).reverse();

    mappingData.unshift({
        id: "JOA",
        value: "A",
        capec: [],
        owasp_appsensor: [],
        owasp_asvs: [],
        owasp_scp: [],
        safecode: []
    });
    mappingData.unshift({
        id: "CORNUCOPIA",
        value: "Explanation",
        capec: [],
        owasp_appsensor: [],
        owasp_asvs: [],
        owasp_scp: [],
        safecode: []
    });
</script>

<div class="deck">
    {#each cards as card,index}
    <div style="transform: translate(150%,35%) rotate({-45 + index*10}deg) " class="card-container">
        <CardPreview cardData={cardData} {card} mapping={mappingData[index]}></CardPreview>
    </div>
    {/each}
</div>

<style>
    .card-container
    {
        width : 15%;
        position: absolute;
        transform-origin: bottom left;

    }

    .deck
    {
        overflow: hidden;
        width : 100%;
        height : 100%;
    }

    @media (max-aspect-ratio: 1/1)
    {
        .deck
        {
            display: none;
        }
    }
</style>
