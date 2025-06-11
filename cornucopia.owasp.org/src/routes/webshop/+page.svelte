<script>
    import SvelteMarkdown from 'svelte-markdown'
    import CardVendor from '../../lib/components/cardVendor.svelte';
    import renderers from '$lib/components/renderers/renderers';
    import {readLang, readTranslation} from "$lib/stores/stores";
    /** @type {{data: any}} */
    let { data } = $props();
    let t = readTranslation();
    const lang = readLang();
    let content = data.content.get($lang) || data.content.get('en');
</script>
<svelte:head>
    <title>{$t('webshop.head.title')}</title>
	<meta name="description" content="{$t('webshop.head.description')}" />
	<meta name="keywords" content="{$t('webshop.head.keywords')}" />
    <meta property="og:title" content="{$t('webshop.head.title')}">
    <meta property="og:description" content="{$t('webshop.head.description')}">
    <meta name="twitter:title" content="{$t('webshop.head.title')}">
    <meta name="twitter:description" content="{$t('webshop.head.description')}">
</svelte:head>
<div>
{#if content != ''}
    <SvelteMarkdown {renderers} source={content}></SvelteMarkdown>
{/if}
<div class="vendor-container">
    <CardVendor
    vendorName="Agile Stationary"
    logoSource="/images/logo-agile-stationary.png"
    productImageSource="/images/owasp-cornucopia-preview.png"
    webshopLink="https://cybersecgames.com/products/owasp-cornucopia-2-1-website-app-edition-threat-modeling-cards">
    </CardVendor>

    <CardVendor
    vendorName="dotNET lab"
    logoSource="/images/logo-dotNET-lab.png"
    productImageSource="/images/dotNET-lab-preview.png"
    webshopLink="https://webshop.dotnetlab.eu/product/cornucopia-card-deck/">
    </CardVendor>
</div>
</div>
<style>
    .vendor-container
    {
        display:flex;
        justify-content: space-between;
        overflow: none;
    }
    @media (max-aspect-ratio: 1/1)
    {
        
        .vendor-container {
            flex-direction: column;
            margin: auto;
            margin-top: 2rem;
            font-size: 1.2rem;
        }
        div
        {
            margin: 0rem 1rem;
        }
    }

</style>
