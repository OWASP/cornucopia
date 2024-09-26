<script lang="ts">
    import CardPreview from "../cardPreview.svelte";
    import type { Suit } from "../../../domain/suit/suit";
    import type { Card } from "../../../domain/card/card";

    export let suits : Suit[];
    // Get a card from every suit
    let cards : Card[] = suits.map((suit) => suit.cards[0]).reverse()
</script>


<div class="deck">
    {#each cards as card,index}
    <div style="transform: translate(150%,35%) rotate({-45 + index*10}deg) " class="card-container">
        <CardPreview card={card}></CardPreview>
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


