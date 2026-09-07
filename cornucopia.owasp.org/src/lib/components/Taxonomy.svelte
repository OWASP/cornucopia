<script lang="ts">
    import { GetCardAttacks, type Attack } from "$lib/cardAttacks";
    import ASVSOverview from "$lib/components/ASVSOverview.svelte";
    import CapecMapTable from "$lib/components/capecMapTable.svelte";
    import { DevGuideMapping } from "$lib/devguideMapping";
    import MappingsList from "$lib/components/mappingsList.svelte";
    import type { Card } from "../../domain/card/card";
    import { readTranslation} from "$lib/stores/stores";
    import {
        getMappingLabel,
        MappingController,
        type MappingLabels,
    } from "../../domain/mapping/mappingController";
    import type { Route } from "../../domain/routes/route";
    import Attacks from "./attacks.svelte";
    import {
        formatTaxonomyValue,
        getTaxonomyDisplayMappings,
    } from "./taxonomyMapping";

    interface Props {
        mappingData: Record<string, unknown>;
        card: Card;
        routes: Map<string, Route[]>;
        capecData?: { [key: number]: { name: string; owasp_asvs: string[] } };
        asvsVersion?: string;
    }
    
    let t = readTranslation();
    let {
        mappingData,
        card,
        routes,
        capecData = undefined,
        asvsVersion = "5.0"
    }: Props = $props();

    const controller = $derived(new MappingController(mappingData));
    let mappings = $derived(controller.getCardMappings(card.id) as Record<string, unknown>);
    let labels = $derived(controller.getLabels());
    let urlTemplates = $derived(controller.getUrlTemplates());
    let attacks: Attack[] = $derived(GetCardAttacks(card.id) as Attack[]);

    function labelFor(attribute: string, mappingLabels: MappingLabels = labels): string | undefined {
        const label = getMappingLabel(mappingLabels, attribute);
        return label === undefined ? undefined : label ? `${label}:` : "";
    }

    function textSTRIDE(input: string | number): string {
        return {
            S: "Spoofing",
            T: "Tampering",
            R: "Repudiation",
            I: "Information Disclosure",
            D: "Denial of Service",
            E: "Elevation of Privilege",
        }[String(input)] || String(input);
    }

    function formatToDoubleDigitSearchString(input: string): string {
        const value = String(input);
        const section = value.lastIndexOf(".") !== -1
            ? value.substring(0, value.lastIndexOf("."))
            : value;
        return section.split(".").map((part) => part.padStart(2, "0")).join(".");
    }

    function linkASVS(input: string | number): string {
        const value = String(input).split("-")[0];
        const asvsRoutes = routes.get("ASVSRoutes") ?? [];
        const searchString = formatToDoubleDigitSearchString(value);
        const result = asvsRoutes.find((route) => route.Section === searchString);
        return result ? `${result.Path.toLowerCase()}#V${value}` : "";
    }

    function linkDevGuide(input: string | number): string {
        return DevGuideMapping.getUrl(String(input));
    }

    function isRecord(value: unknown): value is Record<string, unknown> {
        return typeof value === "object" && value !== null && !Array.isArray(value);
    }

    let displayMappings = $derived(getTaxonomyDisplayMappings(mappings, labels));

    let hasMappings = $derived(displayMappings.length > 0 || mappings.owasp_asvs !== undefined);
    let hasCapecMap = $derived(
        isRecord(mappings.capec_map) &&
        Object.keys(mappings.capec_map).length > 0 &&
        capecData !== undefined,
    );
    let asvsOverviewMappings = $derived(
        Array.isArray(mappings.owasp_asvs)
            ? [...new Set(mappings.owasp_asvs.map((mapping) => Number(String(mapping).split(".").slice(0, 2).join("."))))]
            : [],
    );
</script>

{#if hasMappings}
    <h2 id="mapping" class="title">{$t('cards.mapping.h1.1')}</h2>
    {#if mappings.owasp_asvs !== undefined}
        <MappingsList
            title={labelFor("owasp_asvs") || "OWASP ASVS:"}
            mappings={formatTaxonomyValue(mappings.owasp_asvs)}
            linkFunction={linkASVS}
        />
    {/if}
    {#if mappings.owasp_dev_guide !== undefined}
        <MappingsList
            title={labelFor("owasp_dev_guide") || "OWASP DevGuide:"}
            mappings={formatTaxonomyValue(mappings.owasp_dev_guide)}
            linkFunction={linkDevGuide}
        />
    {/if}
    {#each displayMappings as mapping (mapping.attribute)}
        <MappingsList
            title={mapping.label}
            mappings={mapping.values}
            mappingAttribute={mapping.attribute}
            {urlTemplates}
            textFunction={mapping.attribute === "stride" ? textSTRIDE : undefined}
        />
    {/each}
{:else}
    <h2 id="mapping" class="title">{$t('cards.mappings.no_mappings')}</h2>
{/if}

{#if hasCapecMap && capecData}
    <h2 class="title">{labelFor("capec_map") || "CAPEC Map"}</h2>
    <CapecMapTable
        capecMap={mappings.capec_map as { [key: number]: { owasp_asvs: string[] } }}
        {capecData}
        {linkASVS}
    />
{/if}

{#if card.edition === "webapp" && asvsOverviewMappings.length > 0}
    <h2 class="title">ASVS ({asvsVersion}) Cheat Sheet Series Index</h2>
    <ASVSOverview mappings={asvsOverviewMappings} version={asvsVersion} />
{/if}

<h2 class="title">{$t('cards.mapping.h1.2')}</h2>
<Attacks {attacks} />

<style>
    .title {
        background: var(--background);
        color: white;
        padding: 0.5rem;
    }
</style>
