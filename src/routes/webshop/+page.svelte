<script>
    import CardVendor from '../../lib/components/cardVendor.svelte';
</script>


<div class="page-container">
    <h1>Webshop</h1>
    <p>
        While the easiest way to get started with OWASP Cornucopia is by <a href="/printing">printing</a> out the cards yourself, it is also possible to purchase the cards online.
        OWASP no longer has a stock of printed decks. OWASP does not endorse or recommend commercial products or services. However, following companies do offer a card deck available for online purchase:
    <p>
        <a href="https://agilestationery.com/" target="_blank">Agile Stationary</a> offer large print (v1.20) decks at a discount to OWASP Members. They also offer a <a href="https://croupier.agilestationery.co.uk/">croupier</a> to help you distribute cards to team members.
    </p>
    <p>
        <a href="https://dotnetlab.eu/home-en/" target="_blank">DotNET lab</a> sell a printed deck which complements their <a href="https://cornucopia.dotnetlab.eu/">online reference</a>.
    </p>
    <div class="vendor-container">

        <CardVendor 
        logoSource="/images/logo-agile-stationary.png"
        productImageSource="/images/agile-stationary-preview.png"
        webshopLink="https://agilestationery.co.uk/products/owasp-cornucopia-card-deck-ecommerce-website-edition">
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
        outline: 1xp red solid;
        justify-content: space-between;
        overflow: none;
    }

    .page-container
    {
        padding : 2rem;
        width : 60%;
        margin: auto;
        margin-top: 2rem;
        font-size: 1.2rem;
    }
        @media (max-aspect-ratio: 1/1)
        {
            .page-container
            {
                width : 90%;
            }

            .vendor-container
            {
                flex-direction: column;
            }

        }
    a,p
    {
        font-size: 1.3rem;
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