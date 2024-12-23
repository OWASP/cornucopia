<script>
    import SvelteMarkdown from 'svelte-markdown'
    import CardVendor from '../../lib/components/cardVendor.svelte';
    import renderers from '$lib/components/renderers/renderers';
    import {readLang} from "$lib/stores/stores";
    export let data;
    const lang = readLang();
    let content = data.content.get($lang) || data.content.get('en');
</script>


{#if content != ''}
    <SvelteMarkdown {renderers} source={content}></SvelteMarkdown>
{/if}
<div class="vendor-container">

    <CardVendor 
    logoSource="/images/logo-agile-stationary.png"
    productImageSource="/images/agile-stationary-preview.png"
    webshopLink="https://agilestationery.com/search?q=cornucopia">
    </CardVendor>

    <CardVendor 
    logoSource="/images/logo-dotNET-lab.png"
    productImageSource="/images/dotNET-lab-preview.png"
    webshopLink="https://webshop.dotnetlab.eu/product/cornucopia-card-deck/">
    </CardVendor>
</div>

<style>
    .vendor-container
    {
        display:flex;
        outline: 1xp red solid;
        justify-content: space-between;
        overflow: none;
    }
    @media (max-aspect-ratio: 1/1)
    {

        .vendor-container
        {
            flex-direction: column;
        }

    }

</style>