<script lang="ts">
    import CardPreview from "$lib/components/cardPreview.svelte";
    import {Text} from "$lib/utils/text.js"
    import type { Card } from "../../domain/card/card.js";
    import { MappingController } from "../../domain/mapping/mappingController.js";

    export let data;
    let version : string = "webapp";
    let card : string;
    let suit : string;
    let currentCard : Card = data.cards[0];
    let mapping = (new MappingController(data.mappingData)).getCardMappings(currentCard.id);

    let map : Map<string,boolean> = new Map();
    for(let i = 0 ; i < data.suits.length ; i++)
    {
        map.set(data.suits[i].name,false);
    }

    function toggle(suit : string)
    {
        let value : boolean = map.get(suit) || false;
        map.set(suit,!value);
        map = map;
    }

    function enter(suitParam : string, cardParam : string)
    {
        suit = suitParam;
        card = cardParam;
        if(version == 'webapp')
            currentCard = data.cards.find(card => card.suit == suitParam && card.id == cardParam) ?? {} as Card

        if (version == 'mobileapp')
            currentCard = data.cardsMobile.find(card => card.suit == suitParam && card.id == cardParam) ?? {} as Card

        
        mapping = (new MappingController(data.mappingData)).getCardMappings(currentCard.id);
    }
</script>


<p>
    <button on:click={()=>version = 'webapp'}>Webapp version</button>
    <button on:click={()=>version = 'mobileapp'}>Mobile version</button>
</p>

{#each data.suits as suit}
    {#each suit.cards as card}
        <p><a style="display:none;" href="{card.url}">{suit.name} {card.id}</a></p>
    {/each}
{/each}

<div class="container">
    <div class="tree">

        {#if version == 'webapp'}
            <h1>Web app version</h1>
            {#each data.suits as suit}
                <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
                <h2 on:keypress="{()=>toggle(suit.name)}" on:click="{()=>toggle(suit.name)}">└── {Text.Format(suit.name)}</h2>
                {#if map.get(suit.name)}
                    {#each suit.cards as card}
                        <p on:mouseenter={()=>{enter(suit.name,card.id)}}>
                            <a href="{card.url}">├── {card.id}</a>
                        </p>
                    {/each}
                {/if}
            {/each}
        {/if}

        {#if version == 'mobileapp'}
            <h1>Mobile version</h1>
            {#each data.suitsMobile as suit}
                <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
                <h2 on:keypress="{()=>toggle(suit.name)}" on:click="{()=>toggle(suit.name)}">└── {Text.Format(suit.name)}</h2>
                {#if map.get(suit.name)}
                    {#each suit.cards as card}
                        <p on:mouseenter={()=>{enter(suit.name,card.id)}}>
                            <a href="{card.url}">├── {card.id}</a>
                        </p>
                    {/each}
                {/if}
            {/each}
        {/if}
    </div>
    <div class="preview-container">
            <CardPreview card={currentCard} cardData={data.cardData} {mapping}></CardPreview>
    </div>
</div>

<style>
    .preview-container
    {
        padding-top: 5rem;
        width : 20%;
    }

    .container
    {
        display: flex;
        flex-direction: row;
        width : 100%;
        height : 100%;
        margin-bottom: 50vh;
    }

    h2
    {
        padding-left: 1rem;
        margin:0;
        cursor:pointer;
    }

    h2:hover
    {
        opacity: 50%;
    }

    .tree
    {
        padding : 1rem;
        width : 50%;
    }

    p,h1,a,h2 {
        font-weight: bold;
    }

    p
    {
        margin:0;
        padding : 0rem;
        margin-left: 3rem;
        width : 100%;
    }

    p:hover
    {
        background-color: rgba(255,255,255,.1);
    }

    a
    {
        text-decoration: none;
        color:black;
    }

    a:hover
    {
        opacity: 50%;
    }

    @media (max-aspect-ratio: 1/1) 
    {
        .tree
        {
            width : 100%;
        }

        .preview-container
        {
            display: none;
        }
    }
</style>
