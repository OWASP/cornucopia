<script lang="ts">
    interface Props {
        vendorName: string,
        logoSource: string;
        productImageSource: string;
        webshopLink: string;
    }

    let { logoSource, productImageSource, webshopLink, vendorName }: Props = $props();
</script>

<div class="vendor">
    <div class="image-container">
        <img class="logo-image" alt="{vendorName}'s vendor logo" src={logoSource}/>
    </div>
    <a rel="noopener nofollow" title="Go to {vendorName}'s OWASP Cornucopia vendor webshop" target="_blank" href={webshopLink}><img alt="{vendorName}'s OWASP Cornucopia box of cards" title="{vendorName}'s OWASP Cornucopia box of cards" class="product-image" src={productImageSource}/></a>
    <a rel="noopener nofollow" title="Go to {vendorName}'s OWASP Cornucopia vendor webshop" class="shop-link" target="_blank" href={webshopLink}>Visit external webshop</a>
</div>

<style>
    .shop-link
    {
        text-align: center;
        width: 100%;
        margin-bottom: 1rem;
    }

    .image-container
    {
        background-color: var(--background);
        border-top-left-radius: 1rem;
        border-top-right-radius: 1rem;
    }

    .product-image
    {
        width: 100%;
    }

    .logo-image
    {
        width: 40%;
        display: block;
        margin:auto;
    }
    .vendor
    {
        width: 45%;
        outline: 1px rgb(205, 205, 205) solid;
        border-radius: 1rem;
        box-shadow: var(--box-shadow);
    }

        @media (max-aspect-ratio: 1/1)
        {
            .vendor
            {
                width: 100%;
                margin-bottom: 2rem;
            }

        }
    a
    {
        font-size: 1.2rem;
        font-family: var(--font-body);
    }

    a
    {
        display: inline-block;
        text-decoration: none;
        font-weight: bold;
        color:var(--background);
    }

    a:hover
    {
        opacity: 70%;
        color: rgb(41, 0, 176);
    }
</style>
