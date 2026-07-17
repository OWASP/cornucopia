<script lang="ts">
  import type { PageData } from "./$types";
  import { Text } from "$lib/utils/text";
  import CardFound from "$lib/components/cardFound.svelte";
  import CardNotFound from "$lib/components/cardNotFound.svelte";
  import type { Card } from "../../../domain/card/card";
  import { isKnownCardId } from "../../../domain/card/cardIds";
  import { readLang, readTranslation } from "$lib/stores/stores";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();
  let _t = readTranslation();
  const lang = $state(readLang());
  const cards = $derived(data.decks.get($lang));
  let card : Card = $derived(cards.get(data.card) as Card);
  let language = $derived($lang ? $lang : data.lang);
  const languages = $derived(data.languages);

  function cardFound()
    {
    return isKnownCardId(card?.id)
  }

  function getEdition(str: string) : string {
    if (str == "webapp") return "Website App Edition";
    if (str == "mobileapp") return "Mobile App Edition";
    if (str == "companion") return "Companion Edition";
    if (str == "eop") return "Elevation of Privilege Edition";
    return str;
  }
</script>
<svelte:head>
  {#if cardFound()}
    <link rel="canonical" href="https://cornucopia.owasp.org/card/{card.edition}/{card.id}" />
    <title>OWASP Cornucopia - {getEdition(card.edition)} - {Text.convertToTitleCase(card.suitName)} ({card.id})</title>
    <meta name="description" content="{card.desc}" />
	  <meta name="keywords" content="OWASP, Cornucopia,{card.edition}, {Text.convertToTitleCase(card.suitName)}, {card.id}" />
    <meta property="og:title" content="OWASP Cornucopia - {getEdition(card.edition)} - {card.name}">
    <meta property="og:description" content="{card.desc}">
    <meta name="twitter:title" content="OWASP Cornucopia - {getEdition(card.edition)} - {card.name}">
    <meta name="twitter:description" content="{card.desc}">
  {/if}
</svelte:head>
<div>
{#if cardFound()}
<CardFound
  routes={data.routes}
  {cards}
  {card}
  versions={data.versions}
  mappingData={data.mappingData.get(card.edition)}
  {languages}
  {language}
  capecData={data.capecData}
/>

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
