<script lang="ts">
  import { Text } from "$lib/utils/text";
  import CardFound from "$lib/components/cardFound.svelte";
  import CardNotFound from "$lib/components/cardNotFound.svelte";
  import type { Card } from "$domain/card/card";
  import type { PageData } from "./$types";
  import { goto } from "$app/navigation";
  import LanguagePicker from "$lib/components/languagePicker.svelte";

  // Props from server load
  let { data }: { data: PageData } = $props();

  let card: Card | undefined = data.cards.get(data.card);

  function cardFound(): boolean {
    const cards_options = [
      "AAA","AA2","AA3","AA4","AA5","AA6","AA7","AA8","AA9","AAX","AAJ","AAQ","AAK",
      "ATA","AT2","AT3","AT4","AT5","AT6","AT7","AT8","AT9","ATX","ATJ","ATQ","ATK",
      "AZA","AZ2","AZ3","AZ4","AZ5","AZ6","AZ7","AZ8","AZ9","AZX","AZJ","AZQ","AZK",
      "CA","C2","C3","C4","C5","C6","C7","C8","C9","CX","CJ","CQ","CK",
      "CMA","CM2","CM3","CM4","CM5","CM6","CM7","CM8","CM9","CMX","CMJ","CMQ","CMK",
      "CRA","CR2","CR3","CR4","CR5","CR6","CR7","CR8","CR9","CRX","CRJ","CRQ","CRK",
      "CRMA","CRM2","CRM3","CRM4","CRM5","CRM6","CRM7","CRM8","CRM9","CRMX","CRMJ","CRMQ","CRMK",
      "NSA","NS2","NS3","NS4","NS5","NS6","NS7","NS8","NS9","NSX","NSJ","NSQ","NSK",
      "PCA","PC2","PC3","PC4","PC5","PC6","PC7","PC8","PC9","PCX","PCJ","PCQ","PCK",
      "RSA","RS2","RS3","RS4","RS5","RS6","RS7","RS8","RS9","RSX","RSJ","RSQ","RSK",
      "SMA","SM2","SM3","SM4","SM5","SM6","SM7","SM8","SM9","SMX","SMJ","SMQ","SMK",
      "VEA","VE2","VE3","VE4","VE5","VE6","VE7","VE8","VE9","VEX","VEJ","VEQ","VEK",
      "JOA","JOB","JOAM","JOBM","CORNUCOPIA"
    ];
    return card ? cards_options.includes(card.id) : false;
  }

function changeVersion(v: string) {
  goto(`/edition/${data.edition}/${data.card}/${v}/en`);
}


  function getEdition(str: string): string {
    if (str === "webapp") return "Website App Edition";
    if (str === "mobileapp") return "Mobile App Edition";
    return str;
  }
</script>

<svelte:head>
  {#if cardFound()}
    <link rel="canonical" href="https://cornucopia.owasp.org/cards/{card.id}" />
    <title>OWASP Cornucopia - {getEdition(card.edition)} - {Text.convertToTitleCase(card.suitName)} ({card.id})</title>
    <meta name="description" content="{card.desc}" />
    <meta name="keywords" content="OWASP, Cornucopia,{card.edition}, {Text.convertToTitleCase(card.suitName)}, {card.id}" />
    <meta property="og:title" content="OWASP Cornucopia - {getEdition(card.edition)} - {card.name}">
    <meta property="og:description" content="{card.desc}">
    <meta name="twitter:title" content="OWASP Cornucopia - {getEdition(card.edition)} - {card.name}">
    <meta name="twitter:description" content="{card.desc}">
  {/if}
</svelte:head>

{#if cardFound()}
  <div class="selectors">
    {#if data.versions?.length > 0}
      <div class="selector">
        <label>Version:</label>
        <select value={data.version} on:change={(e) => changeVersion((e.target as HTMLSelectElement).value)}>
          {#each data.versions as v}
            <option value={v} selected={v === data.version}>{v}</option>
          {/each}
        </select>
      </div>
    {/if}

    {#if data.languages?.length > 0}
      <LanguagePicker
        edition={data.edition}
        cardId={data.card}
        version={data.version}
        currentLanguage={data.lang}
        languages={data.languages}
      />
    {/if}
  </div>

  <CardFound
    {card}
    cards={data.cards}
    language={data.lang}
    mappingData={data.mappingData.get(data.edition)}
    routes={data.routes}
    capecData={data.capecData}
  />
{:else}
  <CardNotFound card={data.card} />
{/if}

<style>
.selectors {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  align-items: flex-end; /* aligns dropdowns nicely even if labels differ */
}

.selector {
  display: flex;
  flex-direction: column;
  min-width: 150px; /* ensures dropdowns have same width baseline */
}

.selector label {
  font-weight: bold;
  font-size: 0.95rem;
  margin-bottom: 0.5rem; /* space between label and dropdown */
}

.selector select {
  padding: 0.5rem 0.6rem;
  font-size: 0.95rem;
  border: 1px solid var(--background, #333);
  border-radius: 5px;
  background-color: white;
  color: var(--background, #333);
  cursor: pointer;
  width: 100%;
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .selectors {
    flex-direction: column;
    align-items: flex-start;
  }
  .selector {
    width: 100%;
  }
}
</style>
