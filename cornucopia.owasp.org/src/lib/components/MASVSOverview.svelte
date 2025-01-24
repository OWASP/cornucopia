<script lang="ts">
    import {data} from '$lib/parsed';
    import { readTranslation } from "$lib/stores/stores";
    interface Props {
        mappings: number[] | undefined;
    }

    let { mappings }: Props = $props();
    let t = readTranslation();
    let isEmpty = $state(true);

    function getIndex(num : number) : any
    {
        return 'V' + num;
    }

    function getUrl(mapping : number) : string
    {
        let ex : string = "https://cheatsheetseries.owasp.org/IndexMASVS.html#objective"
        let base : string = "https://cheatsheetseries.owasp.org/IndexMASVS.html#";
        let index = mapping.toString().replaceAll('.','');
        let lookupIndex = getIndex(mapping)
        let title = data[lookupIndex as keyof typeof data];
        title = title.toString().toLowerCase().replaceAll(' ','-').replaceAll(',','')
        return base + index + '-' + title
    }

    function getDisplayText(mapping : number) : string
    {
        let lookupIndex = getIndex(mapping)
        return 'MASVS V' + mapping.toString() + ' - ' + data[lookupIndex as keyof typeof data] 
    }

    function hasValidLink(mapping : number) : boolean
    {
        let lookupIndex = getIndex(mapping);
        let title = data[lookupIndex as keyof typeof data];
        if (title)
        {
            isEmpty = false;
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

{#if isEmpty}
    <p>{$t('cards.MASVSOverview.p1')}</p>
{/if}

<style>
    p,a
    {
        color: var(--background);
        font-weight: 400;
        font-size: 1.5rem;
    }
</style>