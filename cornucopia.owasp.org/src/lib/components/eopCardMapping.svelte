<script lang="ts">
    interface Props {
        mapping: Record<string, unknown>;
        style?: string;
    }

    let { mapping, style = '' }: Props = $props();
    let mappingStyle = $derived(style ? ' ' + style : '');

    let stride = $derived(String(mapping?.stride ?? '') || '-');
</script>

<p class="mapping-title{mappingStyle}">STRIDE</p>
<p class="mapping-value{mappingStyle}">{stride}</p>

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

    @media (max-width: 1024px) {
        .mapping-title.browser-card-container,
        .mapping-value.browser-card-container {
            font-size: 2vw;
            margin-left: 1vw;
            margin-right: 1vw;
        }

        .mapping-title.browser-card-container:first-of-type {
            margin-top: 2vw;
        }
    }
</style>
