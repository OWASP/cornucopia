<script lang="ts">
  import { run } from 'svelte/legacy';
  import { Text } from "$lib/utils/text";
  import {
    GetCardAttacks, type Attack } from "$lib/cardAttacks";
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

  interface Props {
    mappingData: any;
    card: Card;
    cards: Map<string, Card>;
    routes: Map<string, Route[]>;
    languages: string[];
    language: string;
    capecData?: any;
  }

  let {
    mappingData,
    card = $bindable(),
    cards,
    routes,
    languages,
    language,
    capecData = undefined
  }: Props = $props();
    
  const controller = $derived(new MappingController(mappingData));
  let t = readTranslation();
  let mappings = $state(controller.getCardMappings(card.id));
  let attacks: Attack[] = $state(GetCardAttacks(card.id));

  run(() => {
    mappings = controller.getCardMappings(card.id);
    attacks = GetCardAttacks(card.id);
  });
</script>
<LanguagePicker 
  edition={card.edition}
  cardId={card.id}
  version={card.version}
  currentLanguage={language}
  {languages}
/>
<div>
  <h1 title="OWASP Cornucopia card {Text.convertToTitleCase(card.suitName)} ({card.id})" class="title">{Text.convertToTitleCase(card.suitName)} ({card.id})</h1>
  <CardBrowser bind:card={card} {cards} mappingData={mappings}></CardBrowser>
  <a title="How to play OWASP Cornucopia" class="link" href="/how-to-play">{$t('cards.cardFound.a')}</a>
  <Concept card={card}></Concept>
  <Explanation card={card}></Explanation>
  {#if card.edition == 'webapp'}
  <WebAppCardTaxonomy bind:card={card} {mappingData} {routes} {capecData}></WebAppCardTaxonomy>
  {/if}
  {#if card.edition == 'mobileapp'}
  <MobileAppCardTaxonomy bind:card={card} {mappingData} {routes}></MobileAppCardTaxonomy>
  {/if}
    {#key card}
        <ViewSourceOnGithub></ViewSourceOnGithub>
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

  .clicable {
    cursor: pointer;
  }
</style>