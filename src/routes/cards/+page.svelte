<script lang="ts">
    import type { PageData } from "./$types";
    import CardPreview from "$lib/components/cardPreview.svelte";
    import {Text} from "$lib/utils/text.js"
    import type { Card } from "../../domain/card/card.js";
    import { MappingController } from "../../domain/mapping/mappingController.js";
    import { readLang } from '$lib/stores/stores';
    import type { Suit } from "../../domain/suit/suit.js";

    export let data: PageData;
    const lang = readLang();

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
<a href="#decks"><h1>The card decks</h1></a>
<section id="decks">
<p class="button-container">
    <button class:button-selected={(version == VERSION_WEBAPP)} on:click={()=>changeVersion(VERSION_WEBAPP)}>Website App version</button>
    <button class:button-selected={version == VERSION_MOBILEAPP} on:click={()=>changeVersion(VERSION_MOBILEAPP)}>Mobile App version</button>
</p>

<p class="text">Both current decks have six suits and there are also two Joker cards. Each suit contains 13 cards 
    (Ace, 2-10, Jack, Queen and King). This page contains the card browser where you can browse through each of the
    cards in the OWASP Cornucopia decks.</p>
</section>
{#each webappSuits as suit}
    {#each suit.cards as card}
        <p><a style="display:none;" href="{cards?.get(card)?.url}">{suit.name} {card}</a></p>
    {/each}
{/each}

<div class="container">
    <div class="tree">

        {#if version == VERSION_WEBAPP}
            <h2>Website App version (previously called Ecommerce Website Edition)</h2>
            <p class="text">
                Instead of EoP’s STRIDE suits, Cornucopia suits for the Website App Edition were selected based on the structure of the 
                OWASP Secure Coding Practices - Quick Reference Guide (SCP). The content was mainly drawn from the SCP but with additional 
                consideration of sections in the <a rel="noopener" href="https://owasp.org/www-project-application-security-verification-standard/">OWASP Application Security Verification Standard</a>, the <a rel="noopener" href="https://owasp.org/www-project-web-security-testing-guide">OWASP Web Security Testing Guide</a> and 
                David Rook's <a rel="noopener" href="https://owasp.org/www-pdf-archive//OWASP-SecureDevPrinciples-David-Rook.pdf">Principles of Secure Development</a>. These provided five suits, and a sixth called “Cornucopia” was created for 
                everything else:
            </p>
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
            <h2>Mobile App version</h2>
            <p class="text">
                The second Cornucopia deck, the “Mobile App Edition”, follows the same principles and game rules as the original 
                OWASP Cornucopia, but has different suits based on the <a rel="noopener" href="https://mas.owasp.org/MASVS/">MASVS categories</a>, 
                in addition to the Cornucopia suit that contains threats related to mobile malware and privacy issues:
            </p>
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
        padding-left: 1rem;
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
    .text
    {
        margin: 1rem;
        font-size: 1.3rem;
        font-family: var(--font-body);
        font-weight: normal;
    }

    h1
    {
        padding-top: 1rem;
        padding-bottom: 1rem;
        font-size: 2rem;
        font-weight: 400;
    }

    h1,h2,h3
    {
        padding-left: 1rem;
        margin:0;
        cursor:pointer;
    }

    h3:hover
    {
        opacity: 50%;
    }

    .tree
    {
        padding : 1rem;
        width : 50%;
    }

    p,a,h2,h3 {
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
