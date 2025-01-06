<script lang="ts">
    import CardPreview from "../cardPreview.svelte";
    import type { Suit } from "../../../domain/suit/suit";

    export let suits : Suit[];
    export let cards : any;
    export let mapping : any;

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
    <div style="transform: translate(150%,35%) rotate({-45 + index*10}deg) " class="card-container">
        <CardPreview card={cards.get(card)} mapping={mappingData[index]} hero='yes'></CardPreview>
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
        .card-container
        {
            display: none;
        }
    }
</style>
