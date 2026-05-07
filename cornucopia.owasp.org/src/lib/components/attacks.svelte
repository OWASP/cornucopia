<script lang="ts">
    import { resolve } from "$app/paths";
    import { goto } from "$app/navigation";
    import { readTranslation } from "$lib/stores/stores";

    interface Props {
        attacks: Array<{ name: string; url: string }>;
    }

    let { attacks }: Props = $props();
    let t = readTranslation();
</script>

{#each attacks as attack (attack.url)}
    <p>
        <a
            title={attack.name}
            href={resolve('/taxonomy/attacks')}
            on:click|preventDefault={() => goto(resolve('/taxonomy/attacks/' + attack.url))}
        >
            {attack.name}
        </a>
    </p>
{:else}
    <p>{$t('cards.attacks.p1')}</p>
{/each}

<style>
    p {
        font-size: 1.5rem;
    }

    a,
    p {
        color: var(--background);
        font-family: var(--font-title);
        font-weight: 400;
    }
</style>
