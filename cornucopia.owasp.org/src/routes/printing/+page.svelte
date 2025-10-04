<script>
    import SvelteMarkdown from 'svelte-markdown';
    import { renderers }  from '$lib/components/renderers/renderers';
    import {readLang, readTranslation} from "$lib/stores/stores";

    /** @type {{data: any}} */
    let { data } = $props();
    let t = readTranslation();
    const lang = readLang();
    let content = data.content.get($lang) || data.content.get('en');
</script>
<svelte:head>
    <title>{$t('printing.head.title')}</title>
    <link rel="canonical" href="https://cornucopia.owasp.org/printing" />
    <meta name="description" content="{$t('printing.head.description')}" />
	<meta name="keywords" content="{$t('printing.head.keywords')}" />
    <meta property="og:title" content="{$t('printing.head.title')}">
    <meta property="og:description" content="{$t('printing.head.description')}">
    <meta name="twitter:title" content="{$t('printing.head.title')}">
    <meta name="twitter:description" content="{$t('printing.head.description')}">
</svelte:head>
<div>
{#if content != ''}
<SvelteMarkdown {renderers} source={content}></SvelteMarkdown>
{/if}
</div>
<style>
    @media (max-aspect-ratio: 1/1)
    {
        div
        {
            margin: 0rem 1rem;
        }
    }
</style>
