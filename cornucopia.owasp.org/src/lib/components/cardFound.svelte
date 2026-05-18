<script lang="ts">
  import { Text } from "$lib/utils/text";
  import {GetCardAttacks, type Attack } from "$lib/cardAttacks";
  import Explanation from "./explanation.svelte";
  import CardBrowser from "$lib/components/cardBrowser.svelte";
  import type { Card } from "$domain/card/card";
  import ViewSourceOnGithub from "$lib/components/viewSourceOnGithub.svelte";
  import type { Route } from "$domain/routes/route";
  import { MappingController } from "$domain/mapping/mappingController";
  import WebAppCardTaxonomy from "./webAppCardTaxonomy.svelte";
  import LanguagePicker from "$lib/components/languagePicker.svelte";
  import MobileAppCardTaxonomy from "./mobileAppCardTaxonomy.svelte";
  import { readTranslation } from "$lib/stores/stores";
  import Concept from './concept.svelte';
  import CompanionCardTaxonomy from './companionCardTaxonomy.svelte';

  interface Props {
    mappingData: any;
    card: Card;
    cards: Map<string, Card>;
    routes: Map<string, Route[]>;
    languages: string[];
    language: string;
    capecData?: any;
    versions: string[];
  }

  let {
    mappingData,
    card = $bindable(),
    cards,
    routes,
    languages,
    versions,
    language,
    capecData = undefined
  }: Props = $props();
    
  const controller = $derived(new MappingController(mappingData));
  let t = readTranslation();
  let mappings = $derived(controller.getCardMappings(card.id));
  let _attacks: Attack[] = $derived(GetCardAttacks(card.id));
  const asvsVersion = $derived(card.version < '3.0' ? '4.0.3' : '5.0');
</script>
<LanguagePicker 
  edition={card.edition}
  cardId={card.id}
  version={card.version}
  currentLanguage={language}
  {languages}
  {versions}
/>
<div>
  <h1 title="OWASP Cornucopia card {Text.convertToTitleCase(card.suitName)} ({card.id})" class="title">{Text.convertToTitleCase(card.suitName)} ({card.id})</h1>
  <CardBrowser {card} {cards} mappingData={mappings}></CardBrowser>
  <button
    class="copy-link-btn"
    onclick={() => {
      const url = window.location.origin + '/cards/' + card.id;
      if (navigator.clipboard) {
        navigator.clipboard.writeText(url);
      } else {
        const el = document.createElement('textarea');
        el.value = url;
        document.body.appendChild(el);
        el.select();
        document.execCommand('copy');
        document.body.removeChild(el);
      }
    }}
  >
    🔗 {$t('cards.cardFound.copyLink') ?? 'Copy card link'}
  </button>
  <a title="How to play OWASP Cornucopia" class="link" href="/how-to-play">{$t('cards.cardFound.a')}</a>
  <Concept card={card}></Concept>
  <Explanation card={card}></Explanation>
  {#if card.edition == 'webapp'}
  <WebAppCardTaxonomy {card} {mappingData} {routes} {capecData} {asvsVersion}></WebAppCardTaxonomy>
  {/if}
  {#if card.edition == 'mobileapp'}
  <MobileAppCardTaxonomy {card} {mappingData} {routes}></MobileAppCardTaxonomy>
  {/if}
  {#if card.edition == "companion"}
  <CompanionCardTaxonomy {card} {mappingData} {routes}></CompanionCardTaxonomy>
  {/if}
    {#key card}
        <ViewSourceOnGithub path={card.githubUrl}></ViewSourceOnGithub>
    {/key}
</div>

<style>
  p {
    font-size: 1.5rem;
  }
  h1,
  a,
  p {
    color: var(--background);
    font-family: var(--font-title);
    font-weight: 400;
  }

  .link {
    text-align: center;
    width: 100%;
    display: block;
    margin-top: 1rem;
    margin-bottom: 1rem;
    font-size: 1.5rem;
  }

  .title {
    background: var(--background);
    color: white;
    padding: 0.5rem;
    text-transform: uppercase;
  }

  .copy-link-btn {
    display: block;
    margin: 0.5rem auto;
    padding: 0.5rem 1.5rem;
    background: none;
    border: 2px solid var(--background);
    color: var(--background);
    font-family: var(--font-title);
    font-size: 1rem;
    cursor: pointer;
    border-radius: 4px;
    transition: var(--transition);
  }
  .copy-link-btn:hover {
    background: var(--background);
    color: white;
  }
  .clicable {
    cursor: pointer;
  }
</style>
