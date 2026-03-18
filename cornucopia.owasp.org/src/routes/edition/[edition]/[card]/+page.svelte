<script lang="ts">
  import { Text } from "$lib/utils/text";
  import CardFound from "$lib/components/cardFound.svelte";
  import CardNotFound from "$lib/components/cardNotFound.svelte";
  import type { Card } from "$domain/card/card";
  import { readLang, readTranslation } from "$lib/stores/stores";
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();
  let t = readTranslation();
  const lang = $state(readLang());
  let cards = $derived(data.cards);
  let card : Card = $derived(cards.get(data.card) as Card);
  let language = $derived($lang ? $lang : data.lang);
  let versions = $derived(data.versions);

  const languages = $derived(data.languages);

  function cardFound() 
    {
    let cards_options = [
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
      "LLMA","LLM2","LLM3","LLM4","LLM5","LLM6","LLM7","LLM8","LLM9","LLMX","LLMJ","LLMQ","LLMK",
      "AAIA","AAI2","AAI3","AAI4","AAI5","AAI6","AAI7","AAI8","AAI9","AAIX","AAIJ","AAIQ","AAIK",
      "CLDA","CLD2","CLD3","CLD4","CLD5","CLD6","CLD7","CLD8","CLD9","CLDX","CLDJ","CLDQ","CLDK",
      "FREA","FRE2","FRE3","FRE4","FRE5","FRE6","FRE7","FRE8","FRE9","FREX","FREJ","FREQ","FREK",
      "DVOA","DVO2","DVO3","DVO4","DVO5","DVO6","DVO7","DVO8","DVO9","DVOX","DVOJ","DVOQ","DVOK",
      "SEA","SE2","SE3","SE4","SE5","SE6","SE7","SE8","SE9","SEX","SEJ","SEQ","SEK",
      "BOTA","BOT2","BOT3","BOT4","BOT5","BOT6","BOT7","BOT8","BOT9","BOTX","BOTJ","BOTQ","BOTK",
      "JOA","JOB","JOAM","JOBM","CORNUCOPIA"]
    return (cards_options.includes(String(card?.id).toUpperCase()))
  }

  function getEdition(str: string) : string {
    if (str == "webapp") return "Website App Edition";
    if (str == "mobileapp") return "Mobile App Edition";
    if (str == "companion") return "Companion Edition";
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
<div>
{#if cardFound()}
  <CardFound routes={data.routes} {cards} {card} {versions} mappingData={data.mappingData.get(card.edition)} {languages} {language} capecData={data.capecData} />
{:else}
  <CardNotFound card={data.card} />
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
