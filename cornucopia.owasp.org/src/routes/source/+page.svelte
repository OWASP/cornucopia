<script>
    import SvelteMarkdown from 'svelte-markdown';
    import { renderers }  from '$lib/components/renderers/renderers';
    import {readLang, readTranslation} from "$lib/stores/stores";

    export let data;
    let t = readTranslation();
    const lang = readLang();
    let content = data.content.get($lang) || data.content.get('en');
</script>
<svelte:head>
    <title>{$t('source.head.title')}</title>
	<link rel="canonical" href="https://cornucopia.owasp.org/source" />
    <meta name="description" content="{$t('source.head.description')}" />
	<meta name="keywords" content="{$t('source.head.keywords')}" />
    <meta property="og:title" content="{$t('source.head.title')}">
    <meta property="og:description" content="{$t('source.head.description')}">
    <meta name="twitter:title" content="{$t('source.head.title')}">
    <meta name="twitter:description" content="{$t('source.head.description')}">
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
