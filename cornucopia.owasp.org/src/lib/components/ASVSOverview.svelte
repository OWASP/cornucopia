<script lang="ts">
    import { json } from '@sveltejs/kit';
    import {data} from '$lib/parsed';
    import { readTranslation } from "$lib/stores/stores";
    interface Props {
        mappings: number[] | undefined;
    }

    let { mappings }: Props = $props();
    let t = readTranslation();

    function getIndex(num : number) : any
    {
        return 'V' + num;
    }

    function getUrl(mapping : number) : string
    {
        let ex : string = "https://cheatsheetseries.owasp.org/IndexASVS.html#v11-secure-software-development-lifecycle-requirements"
        let base : string = "https://cheatsheetseries.owasp.org/IndexASVS.html#";
        let index = mapping.toString().replaceAll('.','');
        let lookupIndex = getIndex(mapping)
        let title = data[lookupIndex as keyof typeof data];
        title = title.toString().toLowerCase().replaceAll(' ','-').replaceAll(',','')
        return base + 'v' + index + '-' + title
    }

    function getDisplayText(mapping : number) : string
    {
        let lookupIndex = getIndex(mapping)
        return 'ASVS V' + mapping.toString() + ' - ' + data[lookupIndex as keyof typeof data] 
    }

    function hasValidLink(mapping : number) : boolean
    {
        let lookupIndex = getIndex(mapping);
        let title = data[lookupIndex as keyof typeof data];
        if (title)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
</script>

{#if mappings}
    {#each mappings as mapping}
        {#if hasValidLink(mapping)}
            <p>
                <a target="_blank" href="{getUrl(mapping)}">{getDisplayText(mapping)}</a>
            </p>
        {/if}
    {/each}
{/if}

{#if mappings && (mappings.length > 0)}
    <p>{$t('cards.ASVSOverview.p1')}</p>
{/if}

<style>
    p,a
    {
        color: var(--background);
        font-weight: 400;
        font-size: 1.5rem;
    }
</style>