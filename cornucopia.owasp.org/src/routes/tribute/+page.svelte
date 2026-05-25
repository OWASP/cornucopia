<script>
    import SvelteMarkdown from 'svelte-markdown'
    import { renderers } from '$lib/components/renderers/renderers';
    import {readLang, readTranslation} from "$lib/stores/stores";

    /** @type {{data: any}} */
    let { data } = $props();
    let t = readTranslation();
    const lang = readLang();
    let content = $derived(data.content.get($lang) || data.content.get('en'));
</script>
<svelte:head>
    <title>{$t('about.head.title')}</title>
    <link rel="canonical" href="https://cornucopia.owasp.org/tribute" />
    <meta name="description" content="{$t('tribute.head.description')}" />
	<meta name="keywords" content="{$t('tribute.head.keywords')}" />
    <meta property="og:title" content="{$t('tribute.head.title')}">
    <meta property="og:description" content="{$t('tribute.head.description')}">
    <meta name="twitter:title" content="{$t('tribute.head.title')}">
    <meta name="twitter:description" content="{$t('tribute.head.description')}">
</svelte:head>
<div>
{#if content != ''}
    <SvelteMarkdown {renderers} source={content}></SvelteMarkdown>
{/if}
</div>
<style>
    @media (max-width: 767px)
    {
        div
        {
            margin : 0rem 1rem;
        }

    }
</style>
