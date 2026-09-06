<script lang="ts">
    import Metadata from "$lib/components/metadata.svelte";
  import CardFound from "$lib/components/cardFound.svelte";
  import CardNotFound from "$lib/components/cardNotFound.svelte";
  import type { Card } from "$domain/card/card";
  import { readLang, readTranslation } from "$lib/stores/stores";
  import type { PageData } from "./$types";
  type Props = { data: PageData };
  

  let { data }: Props = $props();
  let _t = readTranslation();
  const lang = $state(readLang());
  let cards = $derived(data.cards);
  let card : Card = $derived(cards.get(data.card) as Card);
  let languages = $derived(data.languages);
  let language = $derived($lang ? $lang : data.lang);
  let versions = $derived(data.versions);

  function cardFound()
    {
    return cards?.has(data.card)
  }

</script>
{#if data.metadata}<Metadata metadata={data.metadata} />{/if}
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
