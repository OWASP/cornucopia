<script lang="ts">
    import Metadata from "$lib/components/metadata.svelte";
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
    

    // Derived values that update when data changes
    let content = $derived(data.content.get($lang) || data.content.get('en'));
    let decks = $derived(data?.decks);
    let cards = $derived(decks?.get($lang));
    let suits = $derived(data.suits);
    let mappingData = $derived(data.mappingData);
    let cardImages = $derived(data.cardImages);
    let suitStyling = $derived(data.suitStyling);
    let version = $derived(data?.edition);
    
    let browsableDecks = $derived(data.browsableDecks);
    let currentDeck = $derived(data.currentDeck);
    let cardSuits = $derived.by(() => {
        const key = `${data?.edition}-${$lang}`;
        return suits?.get(key) || suits?.get(`${data?.edition}-en`) as Suit[];
    });
    
    let card = $derived.by(() => {
        if (!cards) return null;
        return cards.get(currentDeck?.defaultPreviewCard ?? 'VE2') as Card;
    });

    let _suit : string;
    let selectedCard = $state<Card | null>(null);
    
    // Use selectedCard if hovering, otherwise use default card
    let displayCard = $derived(selectedCard || card);
    let displayMapping = $derived(displayCard ? (new MappingController(mappingData?.get(version))).getCardMappings(displayCard.id) : []);

    let map : Map<string,boolean> = new SvelteMap();
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
        _suit = suitParam;
        selectedCard = cards?.get(cardParam) as Card;
    }
    
    function changeVersion(versionParam : string)
    {
        // Reset selected card when changing version
        selectedCard = null;
        // Collapse the entire tree down when switching between versions
        setTree(false);
        goto(`/card/${versionParam}`);
    }
</script>
{#if data.metadata}<Metadata metadata={data.metadata} />{/if}
<div>
<section title="OWASP Cornucopia decks" id="decks">
{#if content != ''}
<SvelteMarkdown renderers={renderersForGeneralUse} source={content}></SvelteMarkdown>
{/if}
<p class="button-container script">
    {#each browsableDecks as deck (deck.edition)}
    <button title="OWASP Cornucopia {$t(deck.buttonLabelKey ?? '')}" class:button-selected={version == deck.edition} onclick={()=>changeVersion(deck.edition)}>{$t(deck.buttonLabelKey ?? '')}</button>
    {/each}
</p>
</section>
<div class="script">
    {#each cardSuits as suit (suit.name)}
        {#each suit.cards as card (card)}
                <p><a title="OWASP Cornucopia suit {suit.name}, card {card}" class="card hide" href={cards?.get(card)?.url ?? ''}>{suit.name} {card}</a></p>
        {/each}
    {/each}

    <h2 title="OWASP Cornucopia {$t(currentDeck?.descriptionHeadingKey ?? '')}">{$t(currentDeck?.descriptionHeadingKey ?? '')}</h2>
    <p class="text">
        <!-- eslint-disable-next-line svelte/no-at-html-tags -->
        {@html $t(currentDeck?.descriptionBodyKey ?? '')}
    </p>
    <div class="container">
        <div class="tree">
            {#each cardSuits as suit (suit.name)}
                <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
                <h3 title="OWASP Cornucopia {Text.Format(suit.name).toUpperCase()} suit" onkeypress={()=>toggle(suit.name)} onclick={()=>toggle(suit.name)}>&#x2514;&#9472;&#9472; {Text.Format(suit.name).toUpperCase()}</h3>
                {#if map?.get(suit.name)}
                    {#each suit.cards as card (card)}
                        <p onmouseenter={()=>{enter(suit.name,cards?.get(card)?.id)}}>
                            <a title="OWASP Cornucopia {Text.Format(suit.name).toUpperCase()}, {cards?.get(card)?.id}" href={cards?.get(card)?.url ?? ''}>&#9500;&#9472;&#9472; {cards?.get(card)?.id}</a>
                        </p>
                    {/each}
                {/if}
            {/each}
        </div>
        <div class="preview-container">
                <CardPreview card={displayCard} mapping={displayMapping} {cardImages} {suitStyling} style="preview-card-container"></CardPreview>
        </div>
    </div>
</div>
<noscript>
    <div class="">
        <div>
            <h2 title="OWASP Cornucopia {$t(currentDeck?.descriptionHeadingKey ?? '')}">{$t(currentDeck?.descriptionHeadingKey ?? '')}</h2>
            <p class="text">
                <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                {@html $t(currentDeck?.descriptionBodyKey ?? '')}
            </p>
            {#each cardSuits as suit (suit.name)}
                <label for="{suit.name + '-' + version}" class="suit-button"><span class="label">&#x2514;&#9472;&#9472; {Text.Format(suit.name).toUpperCase()}</span></label>
                <input type=checkbox class="suit-button" id="{suit.name + '-' + version}"/>
                <div class="card-buttons">
                {#each suit.cards as card (card)}
                    <p>
                        <a title="OWASP Cornucopia card: {cards?.get(card)?.id} from suit: {Text.Format(suit.name).toUpperCase()}" href={cards?.get(card)?.url ?? ''}>&#9500;&#9472;&#9472; {cards?.get(card)?.id}</a>
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

    @media (max-width: 767px) 
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





