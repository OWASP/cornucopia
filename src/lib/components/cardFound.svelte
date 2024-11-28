<script lang="ts">
  import {
    GetCardAttacks, type Attack } from "$lib/cardAttacks";
  import AsvsOverview from "$lib/components/ASVSOverview.svelte";
  import MappingsList from "$lib/components/mappingsList.svelte";
  import Utterances from "$lib/components/utterances.svelte";
  import Summary from "./summary.svelte";
  import CardBrowser from "$lib/components/cardBrowser.svelte";
  import type { Card } from "../../domain/card/card";
  import ViewSourceOnGithub from "$lib/components/viewSourceOnGithub.svelte";
  import type { Route } from "../../domain/routes/route";
  import { MappingController, type Mapping } from "../../domain/mapping/mappingController";
  export let mappingData;
  export let card: Card;
  export let cards: Map<string, Card>;
  export let ASVSRoutes: Route[];
  const controller: MappingController = new MappingController(mappingData);
  function linkASVS(input: string) {
    input = String(input).split("-")[0]; // if it's a range of topics, link to the first one
    let routes: Route[] = ASVSRoutes;
    let searchString = FormatToDoubleDigitSearchstring(input);
    let result: Route | undefined = routes.find(
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
  let mappings: Mapping | undefined = controller.getCardMappings(card.id);
  let attacks: Attack[] = GetCardAttacks(card.id);

  $: {
    mappings = controller.getCardMappings(card.id);
    attacks = GetCardAttacks(card.id);
  }
</script>

<div class="container">
  <h1 class="title">{card.name}</h1>
  <p>{card.desc}</p>
  <CardBrowser bind:card={card} {cards} mappingData={mappings}></CardBrowser>
  <a class="link" href="/how-to-play">How to play?</a>
  <Summary card={card}></Summary>
  {#if mappings}
    <h1 class="title">Mappings</h1>
    <MappingsList
      title="Owasp ASVS (4.0):"
      mappings={mappings.owasp_asvs}
      linkFunction={linkASVS}
    />
    <MappingsList
      title="Capec:"
      mappings={mappings.capec}
      linkFunction={linkCapec}
    />
    <MappingsList title="Owasp SCP:" mappings={mappings.owasp_scp} />
    <MappingsList
      title="Owasp Appsensor:"
      mappings={mappings.owasp_appsensor}
    />
    <MappingsList title="Safecode:" mappings={mappings.safecode} />
  {/if}

  <h1 class="title">ASVS (4.0) Cheatsheetseries Index</h1>
  {#if mappings}
    <AsvsOverview mappings={[...new Set (mappings.owasp_asvs.map(s => +String(s).split('.').slice(0, 2).join('.')))]}></AsvsOverview>
  {/if}
  <h1 class="title">Attacks</h1>
  {#each attacks as attack}
    <p><a href="/taxonomy/attacks/{attack.url}">{attack.name}</a></p>
  {/each}

    {#key card}
        <Utterances name={card.suit + '-' + String(card.id).toUpperCase()}></Utterances>
        <ViewSourceOnGithub path="{card.githubUrl}"></ViewSourceOnGithub>
    {/key}
</div>

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

  .link {
    text-align: center;
    width: 100%;
    display: block;
    margin-top: 1rem;
    font-size: 1.5rem;
  }

  .title {
    background: var(--background);
    color: white;
    padding: 0.5rem;
  }

  .container {
    margin: auto;
    width: 60%;
    padding: 1rem;
  }

  @media (max-aspect-ratio: 1/1) {
    .container {
      width: calc(100% - 2rem);
    }
  }
</style>
