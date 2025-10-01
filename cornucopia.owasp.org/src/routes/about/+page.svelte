<script>
    import SvelteMarkdown from 'svelte-markdown'
    import { renderers } from '$lib/components/renderers/renderers';
    import {readLang, readTranslation} from "$lib/stores/stores";

    /** @type {{data: any}} */
    let { data } = $props();
    let t = readTranslation();
    const lang = readLang();
    let content = data.content.get($lang) || data.content.get('en');
</script>
<svelte:head>
    <title>{$t('about.head.title')}</title>
    <meta name="description" content="{$t('about.head.description')}" />
	<meta name="keywords" content="{$t('about.head.keywords')}" />
    <meta property="og:title" content="{$t('about.head.title')}">
    <meta property="og:description" content="{$t('about.head.description')}">
    <meta name="twitter:title" content="{$t('about.head.title')}">
    <meta name="twitter:description" content="{$t('about.head.description')}">
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
            margin : 0rem 1rem;
        }

    }
</style>
