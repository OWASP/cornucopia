<script lang="ts">
  import type { PageData } from "./$types";
  import CardFound from "$lib/components/cardFound.svelte";
  import CardNotFound from "$lib/components/cardNotFound.svelte";
    import type { Card } from "../../../domain/card/card";
    import { readLang } from "$lib/stores/stores";

  export let data: PageData;
  const lang = readLang();
  const cards = data.decks.get($lang);
  let card : Card = cards.get(data.card) as Card;

  function cardFound() 
    {
    let cards_options = [
      "ATA","AT2","AT3","AT4","AT5","AT6","AT7","AT8","AT9","ATX","ATJ","ATQ","ATK",
      "AZA","AZ2","AZ3","AZ4","AZ5","AZ6","AZ7","AZ8","AZ9","AZX","AZJ","AZQ","AZK",
      "CA","C2","C3","C4","C5","C6","C7","C8","C9","CX","CJ","CQ","CK",
      "CRA","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CRX","CRJ","CRQ","CRK",
      "SMA","SM2","SM3","SM4","SM5","SM6","SM7","SM8","SM9","SMX","SMJ","SMQ","SMK",
      "VEA","VE2","VE3","VE4","VE5","VE6","VE7","VE8","VE9","VEX","VEJ","VEQ","VEK",
      "JOA","JOB","CORNUCOPIA",
      "PCA","PC2","PC3","PC4","PC5","PC6","PC7","PC8","PC9","PCX","PCJ","PCQ","PCK",
      "AAA","AA2","AA3","AA4","AA5","AA6","AA7","AA8","AA9","AAX","AAJ","AAQ","AAK",
      "NSA","NS2","NS3","NS4","NS5","NS6","NS7","NS8","NS9","NSX","NSJ","NSQ","NSK",
      "RSA","RS2","RS3","RS4","RS5","RS6","RS7","RS8","RS9","RSX","RSJ","RSQ","RSK",
      "CRMA","CRM2","CRM3","CRM4","CRM5","CRM6","CRM7","CRM8","CRM9","CRMX","CRMJ","CRMQ","CRMK",
      "COMA","COM2","COM3","COM4","COM5","COM6","COM7","COM8","COM9","COMX","COMJ","COMQ","COMK"
      ]
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

<p><a href="/cards">Back to overview</a></p>
{#if cardFound()}
  <CardFound ASVSRoutes={data.ASVSRoutes} {cards} {card}  mappingData={data.mappingData} />
{:else}
  <CardNotFound {card} />
{/if}

<style>
  a {
    font-family: var(--font-title);
    color: var(--white);
    margin: 1rem;
  }
</style>
