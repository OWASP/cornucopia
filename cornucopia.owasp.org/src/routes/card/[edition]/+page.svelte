<script lang="ts">
    import SvelteMarkdown from 'svelte-markdown';
    import { renderersForGeneralUse } from '$lib/components/renderers/renderers';
    import type { PageData } from "./$types";
    import CardPreview from "$lib/components/cardPreview.svelte";
    import {Text} from "$lib/utils/text.js"
    import type { Card } from "$domain/card/card.js";
    import { MappingController } from "$domain/mapping/mappingController.js";
    import { readLang, readTranslation } from '$lib/stores/stores';
    import type { Suit } from "$domain/suit/suit.js";
    import { SvelteMap } from 'svelte/reactivity';
    import { goto } from "$app/navigation";


    interface Props {
        data: PageData;
    }

    let { data }: Props = $props();
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



    let cardSuits = $state(suits?.get(`${data?.edition}-${$lang}`));
    let card : Card = $state(cards?.get('VE2') as Card);
    let version : string = $state(data?.edition);
    if (!(() => cardSuits)()) {
        cardSuits = suits?.get(`${data?.edition}-en`) as Suit[];
    }
    if (version === VERSION_MOBILEAPP) card = cards?.get('PC2') as Card;
    if (version === VERSION_WEBAPP) card = cards?.get('VE2') as Card;

    if (!(() => cards)()) {
        if (version === VERSION_MOBILEAPP) card = cards?.get('PC2') as Card;
        if (version === VERSION_WEBAPP) card = cards?.get('VE2') as Card;
    }

    let suit : string;
    
    let mapping = $state((new MappingController(mappingData?.get((() => version)()))).getCardMappings((() => card)().id));

    let map : Map<string,boolean> = $state(new SvelteMap());
    setTree(false);

    function setTree(expand : boolean)
    {
        // Collapse or expand the entire tree of suits
        for(let i = 0 ; i < (cardSuits?.length as number) ; i++)
        {
            if (cardSuits !== undefined && typeof cardSuits[i] !== 'undefined') map.set(cardSuits[i]?.name,expand);
        }
    }

    function toggle(suit : string)
    {
        let value : boolean = map?.get(suit) || false;
        map.set(suit,!value);
        map = map;
    }

    function enter(suitParam : string, cardParam : string)
    {
        suit = suitParam;
        card = cards?.get(cardParam) as Card;
        mapping = (new MappingController(mappingData?.get(version))).getCardMappings(card.id);
    }
    
    function changeVersion(versionParam : string)
    {
        version = versionParam;
        // Collapse the entire tree down when switching between versions
        setTree(false);
        // Show the following selected cards
        if(version == VERSION_WEBAPP) card = cards?.get('VE2') as Card;
        if(version == VERSION_MOBILEAPP) card = cards?.get('PC2') as Card;
        goto(`/card/${version}`);
    

    }
</script>
<svelte:head>
    <title>{$t('cards.head.title')}</title>
    <link rel="canonical" href={`https://cornucopia.owasp.org/card/${version}`} />
    <meta name="description" content="{$t('cards.head.description')}" />
	<meta name="keywords" content="{$t('cards.head.keywords')}" />
    <meta property="og:title" content="{$t('cards.head.title')}">
    <meta property="og:description" content="{$t('cards.head.description')}">
    <meta name="twitter:title" content="{$t('cards.head.title')}">
    <meta name="twitter:description" content="{$t('cards.head.description')}">
</svelte:head>
<div>
<section title="OWASP Cornucopia decks" id="decks">
{#if content != ''}
<SvelteMarkdown renderers={renderersForGeneralUse} source={content}></SvelteMarkdown>
{/if}
<p class="button-container script">
    <button title="OWASP Cornucopia {$t('cards.button.1')}" class:button-selected={version == VERSION_WEBAPP} onclick={()=>changeVersion(VERSION_WEBAPP)}>{$t('cards.button.1')}</button>
    <button title="OWASP Cornucopia {$t('cards.button.2')}" class:button-selected={version == VERSION_MOBILEAPP} onclick={()=>changeVersion(VERSION_MOBILEAPP)}>{$t('cards.button.2')}</button>
</p>
</section>
<div class="script">
    {#each cardSuits as suit}
        {#each suit.cards as card}
            <p><a title="OWASP Cornucopia suit {suit.name}, card {card}" class="card hide" href="{cards?.get(card)?.url}">{suit.name} {card}</a></p>
        {/each}
    {/each}

    {#if version == VERSION_WEBAPP}
    <h2 title="OWASP Cornucopia {$t('cards.h2.1')}">{$t('cards.h2.1')}</h2>
    <p class="text">
        {@html $t('cards.p2')}
    </p>
    {/if}
    {#if version == VERSION_MOBILEAPP}
    <h2 title="OWASP Cornucopia {$t('cards.h2.2')}">{$t('cards.h2.2')}</h2>
    <p class="text">
        {@html $t('cards.p3')}
    </p>
    {/if}
    <div class="container">
        <div class="tree">
            {#each cardSuits as suit}
                <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
                <h3 title="OWASP Cornucopia {Text.Format(suit.name).toUpperCase()} suit" onkeypress={()=>toggle(suit.name)} onclick={()=>toggle(suit.name)}>└── {Text.Format(suit.name).toUpperCase()}</h3>
                {#if map?.get(suit.name)}
                    {#each suit.cards as card}
                        <p onmouseenter={()=>{enter(suit.name,cards?.get(card)?.id)}}>
                            <a title="OWASP Cornucopia {Text.Format(suit.name).toUpperCase()}, {cards?.get(card)?.id}" href="{cards?.get(card)?.url}">├── {cards?.get(card)?.id}</a>
                        </p>
                    {/each}
                {/if}
            {/each}
        </div>
        <div class="preview-container">
                <CardPreview {card} {mapping} style="preview-card-container"></CardPreview>
        </div>
    </div>
</div>
<noscript>
    <div class="">
        <div>
            {#if version == VERSION_MOBILEAPP}
                <h2 title="OWASP Cornucopia {$t('cards.h2.2')}">{$t('cards.h2.2')}</h2>
                <p class="text">
                    {@html $t('cards.p3')}
                </p>
            {/if}
            {#if version == VERSION_WEBAPP}
                <h2 title="OWASP Cornucopia {$t('cards.h2.1')}">{$t('cards.h2.1')}</h2>
                <p class="text">
                    {@html $t('cards.p2')}
                </p>
            {/if}
            {#each cardSuits as suit}
                <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
                <!-- svelte-ignore a11y_label_has_associated_control -->
                 {#if version == VERSION_WEBAPP}
                    <label for="{suit.name + '-web'}" class="suit-button"><span class="label">└── {Text.Format(suit.name).toUpperCase()}</span></label>
                    <input type=checkbox class="suit-button" id="{suit.name + '-web'}"/>
                {/if}
                {#if version == VERSION_MOBILEAPP}
                    <label for="{suit.name + '-mobile'}" class="suit-button"><span class="label">└── {Text.Format(suit.name).toUpperCase()}</span></label>
                    <input type=checkbox class="suit-button" id="{suit.name + '-mobile'}"/>
                {/if}
                <div class="card-buttons">
                {#each suit.cards as card}
                    <p>
                        <a title="OWASP Cornucopia card: {cards?.get(card)?.id} from suit: {Text.Format(suit.name).toUpperCase()}" href="cards/{cards?.get(card)?.id}">├── {cards?.get(card)?.id}</a>
                    </p>
                {/each}
                </div>
            {/each}
        </div>
    </div>
</noscript>
</div>
<style>

    .card.hide
    {
        display: none;
    }
    .card-buttons {
        display: none;
    }

    .suit-button 
    {
        appearance: none;
    }

    .suit-button:checked + .card-buttons
    {
        display: block;
        margin-bottom: 1rem;
    }

    .card-buttons a 
    {
        text-decoration: none;
    }

    .card-buttons p 
    {
        margin-block-start: 0;
        margin-block-end: 0;
    }

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

    h2,h3,.label
    {
        margin:0;
        cursor:pointer;
    }

    h3:hover,.label
    {
        opacity: 50%;
    }

    .tree
    {
        width : 50%;
    }

    p,a,h2,h3,.label {
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

        div
        {
            margin: 0rem 1rem;
        }
    }
</style>
