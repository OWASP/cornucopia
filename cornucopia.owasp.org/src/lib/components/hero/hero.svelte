<script lang="ts">
    import type { Suit } from "../../../domain/suit/suit";
    import Deck from "../deck/deck.svelte";
    import Chevron from "./chevron.svelte";
    import HeroText from "./heroText.svelte";

    interface Props {
        suits: Suit[];
        cards: any;
        mapping: any;
    }

    let { suits, cards, mapping }: Props = $props();
</script>

<div class="hero">
    <div class="text-container">
        <HeroText></HeroText>
    </div>
    <div class="card-container">
        <Deck {cards} {suits} {mapping}></Deck>
    </div>
    <Chevron href="/#top"></Chevron>
</div>


<style>
    .hero
    {
        display: flex;
        flex-direction: row;
        border-bottom: 1px black solid;
        background-color:hsla(226,100%,7%,1);
        background-image:
        radial-gradient(at 52% 98%, hsla(266, 100%, 32%, 0.305) 0px, transparent 50%),
        radial-gradient(at 2% 83%, hsla(240, 87%, 12%, 0.908) 0px, transparent 50%),
        radial-gradient(at 77% 48%, hsla(175, 56%, 43%, 0.311) 0px, transparent 50%),
        repeating-radial-gradient( circle at 50vw 100vh, transparent 0, #0b2241a8 80px ), repeating-linear-gradient( #0b284f55, #0b284f );   
    }
 
    .card-container
    {
        flex:1;
        margin-top: 8vw;
    }

    .text-container
    {
        flex:1;
        z-index: 50;
        width: 100%
    }

    .hero
    {
        width : 100%;
    }

    

    @media (max-aspect-ratio: 1/1) 
    {
        .hero
        {
            display: flex;
            flex-direction: column;
            height: auto;
        }

        .card-container 
        {
            display: none;
        }
    }
</style>