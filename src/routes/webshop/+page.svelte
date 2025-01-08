<script>
    import SvelteMarkdown from 'svelte-markdown'
    import CardVendor from '../../lib/components/cardVendor.svelte';
    import renderers from '$lib/components/renderers/renderers';
    import {readLang} from "$lib/stores/stores";
    /** @type {{data: any}} */
    let { data } = $props();
    const lang = readLang();
    let content = data.content.get($lang) || data.content.get('en');
</script>
<div>
{#if content != ''}
    <SvelteMarkdown {renderers} source={content}></SvelteMarkdown>
{/if}
<div class="vendor-container">
    <CardVendor 
    logoSource="/images/logo-agile-stationary.png"
    productImageSource="/images/owasp-cornucopia-preview.png"
    webshopLink="https://agilestationery.com/search?q=cornucopia">
    </CardVendor>

    <CardVendor 
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