<script lang="ts">
    import SvelteMarkdown from 'svelte-markdown';
    import renderers from '$lib/components/renderers/renderers';
    import type { PageData } from "./$types";
    import CardPreview from "$lib/components/cardPreview.svelte";
    import {Text} from "$lib/utils/text.js"
    import type { Card } from "../../domain/card/card.js";
    import { MappingController } from "../../domain/mapping/mappingController.js";
    import { readLang, readTranslation } from '$lib/stores/stores';
    import type { Suit } from "../../domain/suit/suit.js";

    export let data: PageData;
    const lang = readLang();
    let t = readTranslation();
    let content = data.content.get($lang) || data.content.get('en');
    let decks = data?.decks;
    let cards = decks?.get($lang);
    let suits = data.suits;
    let mappingData = data.mappingData;

    //TODO move these constants to a more sensible location
    const VERSION_WEBAPP = "webapp"
    const VERSION_MOBILEAPP = "mobileapp"



    let mobileappSuits = suits?.get(`${VERSION_MOBILEAPP}-${$lang}`);
    let webappSuits = suits?.get(`${VERSION_WEBAPP}-${$lang}`);

    if (!mobileappSuits) {
        mobileappSuits = suits?.get(`${VERSION_MOBILEAPP}-en`) as Suit[];
    }

    if (!webappSuits) {
        webappSuits = suits?.get(`${VERSION_WEBAPP}-en`) as Suit[];
    }

    let version : string = VERSION_WEBAPP;
    let suit : string;
    let card : Card = cards?.get('VE2') as Card;
    let mapping = (new MappingController(mappingData?.get(version))).getCardMappings(card.id);

    let map : Map<string,boolean> = new Map();
    setTree(false);

    function setTree(expand : boolean)
    {
        // Collapse or expand the entire tree of suits
        for(let i = 0 ; i < webappSuits.length ; i++)
        {
            map.set(webappSuits[i].name,expand);
        }

        for(let i = 0 ; i < mobileappSuits.length ; i++)
        {
            map.set(mobileappSuits[i].name,expand);
        }
    }

    function toggle(suit : string)
    {
        let value : boolean = map?.get(suit) || false;
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
        card = cards?.get('VE2') as Card;

        if(version == VERSION_MOBILEAPP)
        card = cards?.get('PC2') as Card;

    }


    function enter(suitParam : string, cardParam : string)
    {
        suit = suitParam;
        card = cards?.get(cardParam) as Card;
        mapping = (new MappingController(mappingData?.get(version))).getCardMappings(card.id);
    }
</script>
<section id="decks">
{#if content != ''}
<SvelteMarkdown {renderers} source={content}></SvelteMarkdown>
{/if}
<p class="button-container">
    <button class:button-selected={(version == VERSION_WEBAPP)} on:click={()=>changeVersion(VERSION_WEBAPP)}>{$t('cards.button.1')}</button>
    <button class:button-selected={version == VERSION_MOBILEAPP} on:click={()=>changeVersion(VERSION_MOBILEAPP)}>{$t('cards.button.2')}</button>
</p>
</section>
<div class="script">
    {#each webappSuits as suit}
        {#each suit.cards as card}
            <p><a style="display:none;" href="{cards?.get(card)?.url}">{suit.name} {card}</a></p>
        {/each}
    {/each}

    {#if version == VERSION_WEBAPP}
    <h2>{$t('cards.h2.1')}</h2>
    <p class="text">
        {@html $t('cards.p2')}
    </p>
    {/if}
    {#if version == VERSION_MOBILEAPP}
    <h2>{$t('cards.h2.2')}</h2>
    <p class="text">
        {@html $t('cards.p3')}
    </p>
    {/if}
    <div class="container">
        <div class="tree">

            {#if version == VERSION_WEBAPP}
                
                {#each webappSuits as suit}
                    <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
                    <h3 on:keypress="{()=>toggle(suit.name)}" on:click="{()=>toggle(suit.name)}">└── {Text.Format(suit.name).toUpperCase()}</h3>
                    {#if map?.get(suit.name)}
                        {#each suit.cards as card}
                            <p on:mouseenter={()=>{enter(suit.name, cards?.get(card)?.id)}}>
                                <a href="{cards?.get(card)?.url}">├── {cards?.get(card)?.id}</a>
                            </p>
                        {/each}
                    {/if}
                {/each}
            {/if}

            {#if version == VERSION_MOBILEAPP}
                {#each mobileappSuits as suit}
                    <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
                    <h3 on:keypress="{()=>toggle(suit.name)}" on:click="{()=>toggle(suit.name)}">└── {Text.Format(suit.name).toUpperCase()}</h3>
                    {#if map?.get(suit.name)}
                        {#each suit.cards as card}
                            <p on:mouseenter={()=>{enter(suit.name,cards?.get(card)?.id)}}>
                                <a href="{cards?.get(card)?.url}">├── {cards?.get(card)?.id}</a>
                            </p>
                        {/each}
                    {/if}
                {/each}
            {/if}
        </div>
        <div class="preview-container">
                <CardPreview {card} {mapping}></CardPreview>
        </div>
    </div>
</div>
<noscript>
    <div class="container">
        <div class="tree">
            <h2>{$t('cards.h2-1')}</h2>
            <p class="text">
                {@html $t('cards.p2')}
            </p>
            {#each webappSuits as suit}
                <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
                <h3>└── {Text.Format(suit.name).toUpperCase()}</h3>
                {#each suit.cards as card}
                    <p>
                        <a href="cards/{cards?.get(card)?.id}">├── {cards?.get(card)?.id}</a>
                    </p>
                {/each}
            {/each}
        </div>
        <div class="tree">
            <h2>{$t('cards.h2-2')}</h2>
            <p class="text">
                {@html $t('cards.p3')}
            </p>
            {#each mobileappSuits as suit}
                <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
                <h3 on:keypress="{()=>toggle(suit.name)}" on:click="{()=>toggle(suit.name)}">└── {Text.Format(suit.name).toUpperCase()}</h3>
                {#each suit.cards as card}
                    <p on:mouseenter={()=>{enter(suit.name,cards?.get(card)?.id)}}>
                        <a href="cards/{cards?.get(card)?.id}">├── {cards?.get(card)?.id}</a>
                    </p>
                {/each}
            {/each}
        </div>
    </div>
</noscript>
<style>
    .button-container
    {
        margin-top: 1rem;
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
        padding-left: 1rem;
        width : 40%;
        min-width: 45%;
    }

    .container
    {
        display: flex;
        flex-direction: row;
        width : 100%;
        height : 100%;
        margin-bottom: 50vh;
    }
    .text
    {
        font-size: 1.2rem;
        font-family: var(--font-body);
        font-weight: normal;
    }

    h1
    {
        font-size: 2rem;
        font-weight: 400;
    }

    h1,h2,h3
    {
        margin:0;
        cursor:pointer;
    }

    h3:hover
    {
        opacity: 50%;
    }

    .tree
    {
        width : 50%;
    }

    p,a,h2,h3 {
        font-weight: bold;
    }

    .tree p:hover
    {
        background-color: rgba(255,255,255,.1);
    }

    .tree p
    {
        margin:0;
        padding : 0rem;
        margin-left: 3rem;
        width : 100%;
    }


    .tree a
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
<noscript>
    <style>
        .script
        {
            display: none;
        }
    </style>
</noscript>
