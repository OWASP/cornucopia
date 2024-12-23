<script lang="ts">
    import {
      GetCardAttacks, type Attack } from "$lib/cardAttacks";
    import MASVSOverview from "$lib/components/MASVSOverview.svelte";
    import MappingsList from "$lib/components/mappingsList.svelte";
    import type { Card } from "../../domain/card/card";
    import type { Route } from "../../domain/routes/route";
    import { MappingController, type MobileAppMapping} from "../../domain/mapping/mappingController";
    import MobileAppCardMapping from "./mobileAppCardMapping.svelte";
    import Attacks from "./attacks.svelte";
    import { readTranslation } from "$lib/stores/stores";
    export let mappingData;
    export let card: Card;
    export let routes: Map<string, Route[]>;
    const controller: MappingController = new MappingController(mappingData);
    let t = readTranslation();
    function linkMASVS(input: string) {
      input = String(input).split("-")[0]; // if it's a range of topics, link to the first one
      let ASVSRoutes: Route[] = routes.get('ASVSRoutes') as Route[];
      let searchString = FormatToDoubleDigitSearchstring(input);
      let result: Route | undefined = ASVSRoutes.find(
        (route) => route.Section === searchString
      );
      return result ? result.Path + "#V" + input : "";
    }
  
    function FormatToDoubleDigitSearchstring(input: string) {
      input = String(input)
      let str =
        input.lastIndexOf(".") !== -1
          ? input.substring(0, input.lastIndexOf("."))
          : input;
      let parts = str.split(".").map((part) => part.padStart(2, "0"));
      let searchString = parts.join(".");
      return searchString;
    }
  
    function linkCapec(input: string) {
      return "https://capec.mitre.org/data/definitions/" + input + ".html";
    }
    let mappings: MobileAppMapping = {} as MobileAppCardMapping;
    let attacks: Attack[] = [] as Attack[];
    $: {
      mappings = controller.getMobileAppCardMappings(card.id.replace('CM', 'COM'));
      attacks = GetCardAttacks(card.id) as Attack[] | Attack[];
    }
      
  </script>

    {#if card.value != 'A' && card.value != 'B' }
      <h1 class="title">{$t('cards.mobileAppCardTaxonomy.h1.1')}</h1>
      <MappingsList
        title="OWASP MASVS (4.0):"
        mappings={mappings.owasp_masvs}
        linkFunction={linkMASVS}
      />
      <MappingsList title="OWASP MASTG:" mappings={mappings.owasp_mastg} />
      <MappingsList
        title="Capec:"
        mappings={mappings.capec}
        linkFunction={linkCapec}
      />
      <MappingsList title="Safecode:" mappings={mappings.safecode} />
      {/if}
      <h1 class="title">ASVS (4.0) Cheatsheetseries Index</h1>
      {#if card.value != 'A' && card.value != 'B' }
      <MASVSOverview mappings={[...new Set (mappings.owasp_masvs.map(s => +String(s).split('.').slice(0, 2).join('.')))]}></MASVSOverview>
      {/if}
      <h1 class="title">{$t('cards.mobileAppCardTaxonomy.h1.2')}</h1>
      {#if card.value != 'A' && card.value != 'B' }
      <Attacks {mappings} {attacks}></Attacks>
      {/if}
    
    
  
  <style>
    h1 {
      color: var(--background);
      font-family: var(--font-title);
      font-weight: 400;
    }
  
    .title {
      background: var(--background);
      color: white;
      padding: 0.5rem;
    }
  </style>
  