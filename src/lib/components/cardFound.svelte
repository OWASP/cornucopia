<script lang="ts">
  import { run } from 'svelte/legacy';

  import {
    GetCardAttacks, type Attack } from "$lib/cardAttacks";
  import Summary from "./summary.svelte";
  import CardBrowser from "$lib/components/cardBrowser.svelte";
  import type { Card } from "../../domain/card/card";
  import ViewSourceOnGithub from "$lib/components/viewSourceOnGithub.svelte";
  import type { Route } from "../../domain/routes/route";
  import { MappingController } from "../../domain/mapping/mappingController";
  import WebAppCardTaxonomy from "./webAppCardTaxonomy.svelte";
  import MobileAppCardTaxonomy from "./mobileAppCardTaxonomy.svelte";
  import { readTranslation } from "$lib/stores/stores";
  interface Props {
    mappingData: any;
    card: Card;
    cards: Map<string, Card>;
    routes: Map<string, Route[]>;
  }

  let {
    mappingData,
    card = $bindable(),
    cards,
    routes
  }: Props = $props();
    
  const controller: MappingController = new MappingController(mappingData);
  let t = readTranslation();
  let mappings = $state(controller.getCardMappings(card.id));
  let attacks: Attack[] = $state(GetCardAttacks(card.id));

  run(() => {
    mappings = controller.getCardMappings(card.id);
    attacks = GetCardAttacks(card.id);
  });
</script>

<div>
  <h1 class="title">{card.name}</h1>
  <p>{card.desc}</p>
  <CardBrowser bind:card={card} {cards} mappingData={mappings}></CardBrowser>
  <a class="link" href="/how-to-play">{$t('cards.cardFound.a')}</a>
  <Summary card={card}></Summary>
  {#if card.edition == 'webapp' &&  card.value != 'A' && card.value != 'B'}
  <WebAppCardTaxonomy bind:card={card} {mappingData} {routes}></WebAppCardTaxonomy>
  {/if}
  {#if card.edition == 'mobileapp' &&  card.value != 'A' && card.value != 'B'}
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
    font-size: 1.5rem;
  }

  .title {
    background: var(--background);
    color: white;
    padding: 0.5rem;
  }
</style>