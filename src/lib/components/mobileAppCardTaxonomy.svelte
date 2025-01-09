<script lang="ts">
  import { run } from 'svelte/legacy';

    import {
      GetCardAttacks, type Attack } from "$lib/cardAttacks";
    import MASVSOverview from "$lib/components/MASVSOverview.svelte";
    import MappingsList from "$lib/components/mappingsList.svelte";
    import type { Card } from "../../domain/card/card";
    import type { Route } from "../../domain/routes/route";
    import {MASTG_TESTS_MAPPING} from "../../domain/mapping/mastg";
    import { MappingController, type MobileAppMapping} from "../../domain/mapping/mappingController";
    import MobileAppCardMapping from "./mobileAppCardMapping.svelte";
    import Attacks from "./attacks.svelte";
    import { readTranslation } from "$lib/stores/stores";
    interface Props {
      mappingData: any;
      card: Card;
      routes: Map<string, Route[]>;
    }

    let { mappingData, card = $bindable(), routes }: Props = $props();
    
    const controller: MappingController = new MappingController(mappingData);
    let t = readTranslation();
    function linkMASVS(requirement: string) {
      let parts = String(requirement).split("-");
      let category = 'MASVS-' + parts[0];
      let base = '/taxonomy/masvs-2.1.0/';
      return category ? (base + category.toLowerCase() + '/masvs-' + requirement.toLowerCase() + '#MASVS-' + requirement) : '';
    }

    function linkMASTG(test: string) {
      let base = '/taxonomy/mastg-1.7.0/masvs-';
      return test in MASTG_TESTS_MAPPING ? (base + MASTG_TESTS_MAPPING[test].toLowerCase() + '/mastg-' + test.toLowerCase() + '#MASTG-' + test) : '';
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
    let mappings: MobileAppMapping = $state({} as MobileAppCardMapping);
    let attacks: Attack[] = $state([] as Attack[]);
    run(() => {
      mappings = controller.getMobileAppCardMappings(card.id.replace('CM', 'COM'));
      attacks = GetCardAttacks(card.id) as Attack[] | Attack[];
    });
      
  </script>

    {#if card.value != 'A' && card.value != 'B'}
      <h1 class="title">{$t('cards.mobileAppCardTaxonomy.h1.1')}</h1>
      <MappingsList
        title="OWASP MASVS (2.1):"
        mappings={mappings.owasp_masvs}
        linkFunction={linkMASVS}
      />
      <MappingsList 
        title="OWASP MASTG (1.7):" 
        mappings={mappings.owasp_mastg}
        linkFunction={linkMASTG}
      />
      <MappingsList
        title="Capec:"
        mappings={mappings.capec}
        linkFunction={linkCapec}
      />
      <MappingsList title="Safecode:" mappings={mappings.safecode} />
      {/if}
      <!--<h1 class="title">Cheatsheetseries Index</h1>-->
      {#if card.value != 'A' && card.value != 'B'}
      <!--<MASVSOverview mappings={[...new Set (mappings.owasp_masvs.map(s => +String(s).split('.').slice(0, 2).join('.')))]}></MASVSOverview>-->
      {/if}
      <h1 class="title">{$t('cards.mobileAppCardTaxonomy.h1.2')}</h1>
      {#if card.value != 'A' && card.value != 'B'}
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
  