<script lang="ts">
  import CardFound from "$lib/components/cardFound.svelte";
  import CardNotFound from "$lib/components/cardNotFound.svelte";
  import type { Card } from "$domain/card/card";
  import { isKnownCardId } from "$domain/card/cardIds";
  import type { PageData } from './$types';

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
