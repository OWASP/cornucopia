<script lang="ts">
    import { GetCardAttacks, type Attack } from "$lib/cardAttacks";
    import type { Card } from "../../domain/card/card";
    import type { Route } from "../../domain/routes/route";
    import { MappingController } from "../../domain/mapping/mappingController";
    import MappingsList from "$lib/components/mappingsList.svelte";
    import Attacks from "./attacks.svelte";
    import { readTranslation } from "$lib/stores/stores";

    interface Props {
        mappingData: Record<string, unknown>;
        card: Card;
        routes: Map<string, Route[]>;
    }

    let { mappingData, card = $bindable(), routes: _routes }: Props = $props();

    const controller = $derived(new MappingController(mappingData));
    let t = readTranslation();

    let mappings: Record<string, unknown> = $derived(controller.getCardMappings(card?.id));
    let attacks: Attack[] = $derived(GetCardAttacks(card?.id) as Attack[]);

    function formatValue(val: unknown): string[] {
        if (val === undefined || val === null) return ["-"];
        if (Array.isArray(val))
            return val.length ? val.map((v) => String(v)) : ["-"];
        return [String(val)];
    }
</script>

{#if mappings}
    <h2 id="mapping" class="title">{$t("cards.eopCardTaxonomy.h1.1")}</h2>
    <MappingsList title="STRIDE:" mappings={formatValue(mappings['stride'])} />
    <h2 class="title">{$t("cards.eopCardTaxonomy.h1.2")}</h2>
    {#if attacks}
        <Attacks {attacks} />
    {/if}
{/if}

<style>
    .title {
        background: var(--background);
        color: white;
        padding: 0.5rem;
    }
</style>
