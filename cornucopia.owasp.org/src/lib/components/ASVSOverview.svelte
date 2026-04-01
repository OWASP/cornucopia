<script lang="ts">
    import { onMount } from 'svelte';
    import { readTranslation } from "$lib/stores/stores";

    type AsvsRequirement = {
        section_id: string;
        section_name: string;
    };

    type AsvsPayload = {
        requirements: AsvsRequirement[];
    };

    const ASVS_DATA_URLS = {
        '4.0.3': '/data/asvs-4.0.3/en/OWASP_Application_Security_Verification_Standard_4.0.3.flat.json',
        '5.0': '/data/asvs-5.0/en/OWASP_Application_Security_Verification_Standard_5.0.flat.json'
    } as const;

    let sectionsById = $state(new Map<string, string>());

    function getDataUrlForVersion(inputVersion: string): string {
        return inputVersion === '4.0.3' ? ASVS_DATA_URLS['4.0.3'] : ASVS_DATA_URLS['5.0'];
    }

    async function loadAsvsSections(url: string): Promise<Map<string, string>> {
        try {
            const response = await fetch(url, { method: 'GET' });
            if (!response.ok) {
                return new Map<string, string>();
            }

            const payload = (await response.json()) as AsvsPayload;
            return new Map<string, string>(payload.requirements.map((requirement) => [requirement.section_id, requirement.section_name]));
        } catch {
            return new Map<string, string>();
        }
    }

    interface Props {
        mappings: number[] | undefined;
        version: string;
    }

    let { mappings, version }: Props = $props();

    onMount(async () => {
        sectionsById = await loadAsvsSections(getDataUrlForVersion(version));
    });

    let t = readTranslation();

    function getIndex(num : number) : any
    {
        return 'V' + num;
    }

    function getUrl(mapping : number) : string
    {
        let base : string = "https://cheatsheetseries.owasp.org/IndexASVS.html#";
        let index = mapping.toString().replaceAll('.','');
        let title = getSectionName(mapping);
        title = title.toString().toLowerCase().replaceAll(' ','-').replaceAll(',','')
        
        if (version == '4.0.3')
        {
            index = mapping.toString();
            base = "/taxonomy/cheat-sheets-asvs-4.0.3/#";
            title = title.replace(/,/g, '').split(/[\s-]+/).map((word) => {
                const lowerWord = word.toLowerCase();
                return lowerWord === 'and' ? 'and' : lowerWord.charAt(0).toUpperCase() + lowerWord.slice(1);
            }).join('-') + '-Requirements';
            return base + 'V' + index + '-' + title
        }
        
        
        return base + 'v' + index + '-' + title
    }

    function getSectionName(mapping : number) : string
    {
        let lookupIndex = getIndex(mapping)
        let title = sectionsById.get(lookupIndex);
        return title || '';
    }

    function getDisplayText(mapping : number) : string
    {
        return 'ASVS V' + mapping.toString() + ' - ' + getSectionName(mapping);
    }

    function hasValidLink(mapping : number) : boolean
    {
        return getSectionName(mapping) ? true : false;
    }
</script>

{#if mappings}
    {#each mappings as mapping}
        {#if hasValidLink(mapping)}
            <p>
                <a title="OWASP ASVS {getDisplayText(mapping)}" target="_blank" href="{getUrl(mapping)}">{getDisplayText(mapping)}</a>
            </p>
        {/if}
    {/each}
{/if}

{#if mappings?.length == 0 }
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