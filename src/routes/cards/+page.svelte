<script lang="ts">
    import CardPreview from "$lib/components/cardPreview.svelte";
    import {Text} from "$lib/utils/text.js"
    import type { Card } from "../../domain/card/card.js";
    import { MappingController } from "../../domain/mapping/mappingController.js";

    export let data;

    //TODO move these constants to a more sensible location
    const VERSION_WEBAPP = "webapp"
    const VERSION_MOBILEAPP = "mobileapp"

    let version : string = VERSION_WEBAPP;
    let card : string;
    let suit : string;
    let currentCard : Card = data.cards[0];
    let mapping = (new MappingController(data.mappingData)).getCardMappings(currentCard.id);

    let map : Map<string,boolean> = new Map();
    setTree(false);

    function setTree(expand : boolean)
    {
        // Collapse or expand the entire tree of suits
        for(let i = 0 ; i < data.suits.length ; i++)
        {
            map.set(data.suits[i].name,expand);
        }

        for(let i = 0 ; i < data.suitsMobile.length ; i++)
        {
            map.set(data.suitsMobile[i].name,expand);
        }
    }

    function toggle(suit : string)
    {
        let value : boolean = map.get(suit) || false;
        map.set(suit,!value);
        map = map;
    }

    function changeVersion(versionParam : string)
    {
        version = versionParam;
        // Collapse the entire tree down when switching between versions
        setTree(false);
        // Show the following selected cards
        if(version == VERSION_WEBAPP)
            currentCard = data.cards[1];

        if(version == VERSION_MOBILEAPP)
            currentCard = data.cardsMobile[1];

    }


    function enter(suitParam : string, cardParam : string)
    {
        suit = suitParam;
        card = cardParam;
        if(version == VERSION_WEBAPP)
            currentCard = data.cards.find(card => card.suit == suitParam && card.id == cardParam) ?? {} as Card

        if (version == VERSION_MOBILEAPP)
            currentCard = data.cardsMobile.find(card => card.suit == suitParam && card.id == cardParam) ?? {} as Card

        
        mapping = (new MappingController(data.mappingData)).getCardMappings(currentCard.id);
    }
</script>


<p class="button-container">
    <button class:button-selected={(version == VERSION_WEBAPP)} on:click={()=>changeVersion(VERSION_WEBAPP)}>Webapp version</button>
    <button class:button-selected={version == VERSION_MOBILEAPP} on:click={()=>changeVersion(VERSION_MOBILEAPP)}>Mobile version</button>
</p>

{#each data.suits as suit}
    {#each suit.cards as card}
        <p><a style="display:none;" href="{card.url}">{suit.name} {card.id}</a></p>
    {/each}
{/each}

<div class="container">
    <div class="tree">

        {#if version == VERSION_WEBAPP}
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

        {#if version == VERSION_MOBILEAPP}
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
    .button-container
    {
        margin-top: 1rem;
        margin-left: 1rem;
        width:auto;
    }

    
    button
    {
        font-weight: bold;
        background: none;
        border:none;
        font-size: 1.2rem;
        outline: 1px var(--background) solid;
        color: var(--background);
        background-color: white;
        padding: .5rem;
        cursor:pointer;
    }

    button:hover
    {
        opacity: 50%;
    }

    .button-selected
    {
        outline: 1px var(--background) solid;
        background-color: var(--background);
        color: var(--background);    
        color:white;
    }

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

        button
        {
            width: 90%;
        }
    }
</style>
