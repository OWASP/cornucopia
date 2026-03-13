<script lang="ts">
    interface Props {
        mapping: any;
        style?: string;
    }

    let { mapping, style = '' }: Props = $props();
    let mappingStyle = $derived(style ? ' ' + style : '');

    const NON_DISPLAY = new Set([
        'id', 'value', 'url'
    ]);

    function formatValue(val: any): string {
        if (val === undefined || val === null) return '-';
        if (Array.isArray(val)) return val.length ? val.join(',') : '-';
        return String(val) || '-';
    }

    function toLabel(key: string): string {
        if (key === 'capec') return 'CAPEC™';
        return key
            .replace(/_/g, ' ')
            .toUpperCase();
    }

    let rows = $derived(
        Object.keys(mapping)
            .filter(key => {
                if (NON_DISPLAY.has(key)) return false;
                if (key.endsWith('_print')) return false;
                return true;
            })
            .map(key => ({ label: toLabel(key), value: formatValue(mapping[key]) }))
            
    );
</script>

{#each rows as row}
    <p class="mapping-title{mappingStyle}">{row.label}</p>
    <p class="mapping-value{mappingStyle}">{row.value}</p>
{/each}

<style>
    .mapping-title, .mapping-value {
        font-size: 1.1vw;
        margin: 0;
        margin-left: .25rem;
        margin-right: .25rem;
        word-wrap: break-word;
        white-space: initial;
    }

    .hero-card-container {
        font-size: max(0.3vh, 0.6vw);
    }

    .mapping-title {
        font-weight: bold;
    }

    .mapping-value {
        border-bottom: 1px rgb(192, 192, 192) solid;
    }

    .mapping-title.browser-card-container,
    .mapping-value.browser-card-container {
        font-size: 0.7vw;
        margin-left: 1vw;
        margin-right: 1vw;
    }

    @media (max-aspect-ratio: 1.5/1) {
        .mapping-title.browser-card-container,
        .mapping-value.browser-card-container {
            font-size: 2vw;
            margin-left: 1vw;
            margin-right: 1vw;
        }
    }
</style>