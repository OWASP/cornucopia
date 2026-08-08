<script lang="ts">
  import { Text } from "$lib/utils/text";
  import CardFound from "$lib/components/cardFound.svelte";
  import CardNotFound from "$lib/components/cardNotFound.svelte";
  import type { Card } from "$domain/card/card";
  import { isKnownCardId } from "$domain/card/cardIds";
  import type { PageData } from './$types';
  import { EDITION_FULL_NAMES } from "$lib/services/deckServiceConsts";

  let { data }: { data: PageData } = $props();
  const language = $derived(data?.lang);
  let cards = $derived(data.cards);
  let card : Card = $derived(cards.get(data.card) as Card);
  let languages = $derived(data.languages);
  let versions = $derived(data.versions);

  function cardFound()
    {
    return isKnownCardId(card?.id)
  }
</script>
<svelte:head>
  {#if cardFound()}
    <link rel="canonical" href="https://cornucopia.owasp.org/cards/{card.id}" />
    <title>OWASP Cornucopia - {EDITION_FULL_NAMES[card.edition] ?? card.edition} - {Text.convertToTitleCase(card.suitName)} ({card.id})</title>
    <meta name="description" content="{card.desc}" />
	  <meta name="keywords" content="OWASP, Cornucopia,{card.edition}, {Text.convertToTitleCase(card.suitName)}, {card.id}" />
    <meta property="og:title" content="OWASP Cornucopia - {EDITION_FULL_NAMES[card.edition] ?? card.edition} - {card.name}">
    <meta property="og:description" content="{card.desc}">
    <meta name="twitter:title" content="OWASP Cornucopia - {EDITION_FULL_NAMES[card.edition] ?? card.edition} - {card.name}">
    <meta name="twitter:description" content="{card.desc}">
  {/if}
</svelte:head>
<div>
{#if cardFound()}
  <CardFound routes={data.routes} {cards} {card} {versions} mappingData={data.mappingData.get(card.edition)} {languages} {language} capecData={data.capecData} cardImages={data.cardImages} suitStyling={data.suitStyling} />
{:else}
  <CardNotFound card={data.card} />
{/if}
</div>
<style>
    @media (max-width: 767px) 
    {
        div
        {
            margin: 0rem 1rem;
        }
    }

</style>
