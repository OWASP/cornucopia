<script lang="ts">
    import {
      GetCardAttacks, type Attack } from "$lib/cardAttacks";
    import ASVSOverview from "$lib/components/ASVSOverview.svelte";
    import MappingsList from "$lib/components/mappingsList.svelte";
    import type { Card } from "../../domain/card/card";
    import type { Route } from "../../domain/routes/route";
    import { MappingController, type WebAppMapping } from "../../domain/mapping/mappingController";
    export let mappingData;
    export let card: Card;
    export let routes: Map<string, Route[]>;
    const controller: MappingController = new MappingController(mappingData);
    function linkASVS(input: string) {
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
    let mappings: WebAppMapping = controller.getWebAppCardMappings(card.id);
    let attacks: Attack[] = GetCardAttacks(card.id);
  
    $: {
      mappings = controller.getWebAppCardMappings(card.id);
      attacks = GetCardAttacks(card.id);
    }
  </script>

    {#if card.value != 'A' && card.value != 'B' }
      <h1 class="title">Mappings</h1>
      <MappingsList
        title="OWASP ASVS (4.0):"
        mappings={mappings.owasp_asvs}
        linkFunction={linkASVS}
      />
      <MappingsList
        title="Capec:"
        mappings={mappings.capec}
        linkFunction={linkCapec}
      />
      <MappingsList title="OWASP SCP:" mappings={mappings.owasp_scp} />
      <MappingsList
        title="OWASP Appsensor:"
        mappings={mappings.owasp_appsensor}
      />
      <MappingsList title="Safecode:" mappings={mappings.safecode} />
    {/if}
  
    <h1 class="title">ASVS (4.0) Cheatsheetseries Index</h1>
    {#if card.value != 'A' && card.value != 'B' }
      <ASVSOverview mappings={[...new Set (mappings.owasp_asvs.map(s => +String(s).split('.').slice(0, 2).join('.')))]}></ASVSOverview>
    {/if}
    <h1 class="title">Attacks</h1>
    {#each attacks || [] as attack}
      <p><a href="/taxonomy/attacks/{attack.url}">{attack.name}</a></p>
    {/each}
  
  <style>
    p {
      font-size: 1.5rem;
    }
    h1,
    a,
    p {
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
  