<script lang="ts">
    import CardPreview from "../cardPreview.svelte";
    import type { Suit } from "../../../domain/suit/suit";

    interface Props {
        suits: Suit[];
        cards: any;
        mapping: any;
    }

    let { suits, cards, mapping }: Props = $props();

    // Manual selection of cards to display on the frontpage 
    let selectedCards : string[] =  ["JOA","C7","CR6","AZ5","SM4","VE3","AT2",]  
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
    
</script>

<div class="deck">
    {#each selectedCards as card,index}
    <div class="card-container card-{index}">
        <CardPreview card={cards.get(card)} mapping={mappingData[index]} style='hero-card-container'></CardPreview>
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

    .card-container.card-0
    {
        transform: translate(150%,35%) rotate(-35deg)
    }
    .card-container.card-1
    {
        transform: translate(150%,35%) rotate(-25deg)
    }
    .card-container.card-2
    {
        transform: translate(150%,35%) rotate(-15deg)
    }
    .card-container.card-3
    {
        transform: translate(150%,35%) rotate(-5deg)
    }
    .card-container.card-4
    {
        transform: translate(150%,35%) rotate(5deg)
    }
    .card-container.card-5
    {
        transform: translate(150%,35%) rotate(15deg)
    }
    .card-container.card-6
    {
        transform: translate(150%,35%) rotate(25deg)
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
        .card-container
        {
            display: none;
        }
    }
</style>
