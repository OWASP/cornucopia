<script lang="ts">
    import { run } from "svelte/legacy";
    import { GetCardAttacks, type Attack } from "$lib/cardAttacks";
    import type { Card } from "../../domain/card/card";
    import type { Route } from "../../domain/routes/route";
    import { MappingController } from "../../domain/mapping/mappingController";
    import MappingsList from "$lib/components/mappingsList.svelte";
    import Attacks from "./attacks.svelte";
    import { readTranslation } from "$lib/stores/stores";

    interface Props {
        mappingData: any;
        card: Card;
        routes: Map<string, Route[]>;
    }

    let { mappingData, card = $bindable(), routes }: Props = $props();

    const controller = $derived(new MappingController(mappingData));
    let t = readTranslation();

    let mappings: any = $state({});
    let attacks: Attack[] = $state([]);

    run(() => {
        mappings = controller.getCardMappings(card?.id);
        attacks = GetCardAttacks(card?.id) as Attack[];
    });

    const NON_DISPLAY = new Set(["id", "value", "url"]);

    function formatValue(val: any): string[] {
        if (val === undefined || val === null) return ["-"];
        if (Array.isArray(val))
            return val.length ? val.map((v) => String(v)) : ["-"];
        return [String(val)] || ["-"];
    }

    function toLabel(key: string): string {
        return key.replace(/_/g, " ").toUpperCase() + ":";
    }

    let displayMappings = $derived(
        Object.keys(mappings || {})
            .filter((key) => {
                if (NON_DISPLAY.has(key)) return false;
                if (key.endsWith("_print")) return false;
                return true;
            })
            .map((key) => ({
                label: toLabel(key),
                values: formatValue(mappings[key]),
            })),
    );
</script>

{#if mappings}
    <h1 class="title">{$t("cards.companionCardTaxonomy.h1.1")}</h1>
    {#each displayMappings as mapping}
        <MappingsList title={mapping.label} mappings={mapping.values} />
    {/each}
    <h1 class="title">{$t("cards.companionCardTaxonomy.h1.2")}</h1>
    {#if attacks}
        <Attacks {mappings} {attacks} />
    {/if}
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
