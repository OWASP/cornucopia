<script lang="ts">
  import type { PageData } from "./$types";
  import CardFound from "$lib/components/cardFound.svelte";
  import CardNotFound from "$lib/components/cardNotFound.svelte";
  import type { Card } from "../../../domain/card/card";
  import { readLang, readTranslation } from "$lib/stores/stores";

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();
  const lang = readLang();
  let t = readTranslation();
  const cards = data.decks.get($lang);
  let card : Card = cards.get(data.card) as Card;

  function cardFound() 
    {
    let cards_options = [
      "AAA","AA2","AA3","AA4","AA5","AA6","AA7","AA8","AA9","AAX","AAJ","AAQ","AAK",
      "ATA","AT2","AT3","AT4","AT5","AT6","AT7","AT8","AT9","ATX","ATJ","ATQ","ATK",
      "AZA","AZ2","AZ3","AZ4","AZ5","AZ6","AZ7","AZ8","AZ9","AZX","AZJ","AZQ","AZK",
      "CA","C2","C3","C4","C5","C6","C7","C8","C9","CX","CJ","CQ","CK",
      "CMA","CM2","CM3","CM4","CM5","CM6","CM7","CM8","CM9","CMX","CMJ","CMQ","CMK",
      "COMA","COM2","COM3","COM4","COM5","COM6","COM7","COM8","COM9","COMX","COMJ","COMQ","COMK",
      "CRA","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CRX","CRJ","CRQ","CRK",
      "CRMA","CRM2","CRM3","CRM4","CRM5","CRM6","CRM7","CRM8","CRM9","CRMX","CRMJ","CRMQ","CRMK",
      "NSA","NS2","NS3","NS4","NS5","NS6","NS7","NS8","NS9","NSX","NSJ","NSQ","NSK",
      "PCA","PC2","PC3","PC4","PC5","PC6","PC7","PC8","PC9","PCX","PCJ","PCQ","PCK",
      "REA","RE2","RE3","RE4","RE5","RE6","RE7","RE8","RE9","REX","REJ","REQ","REK",
      "SMA","SM2","SM3","SM4","SM5","SM6","SM7","SM8","SM9","SMX","SMJ","SMQ","SMK",
      "VEA","VE2","VE3","VE4","VE5","VE6","VE7","VE8","VE9","VEX","VEJ","VEQ","VEK",
      "JOA","JOB","JOAM","JOBM","CORNUCOPIA"]
    let suits_options = [
      "data-validation-&-encoding",
      "authentication",
      "session-management",
      "authorization",
      "cryptography",
      "cornucopia",
      "wild-card",
      "about",
      "platform-&-code",
      "authentication-&-authorization",
      "network-&-storage",
      "resilience",
    ]
    return (cards_options.includes(String(card.id).toUpperCase()) && suits_options.includes(card.suitName.toLowerCase().replaceAll(' ', '-')))
  }
</script>
<div>
{#if cardFound()}
  <CardFound routes={data.routes} {cards} {card}  mappingData={data.mappingData.get(card.edition)} />
{:else}
  <CardNotFound {card} />
{/if}
</div>
<style>
    @media (max-aspect-ratio: 1/1) 
    {
        div
        {
            margin: 0rem 1rem;
        }
    }

</style>