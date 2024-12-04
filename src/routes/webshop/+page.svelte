<script>
    import CardVendor from '../../lib/components/cardVendor.svelte';
</script>


<div class="page-container">
    <h1>Web shop</h1>
    <p>
        While the easiest way to get started with OWASP Cornucopia is by <a href="/printing">printing</a> out the cards yourself, it is also possible to purchase the cards online.
        OWASP no longer has a stock of printed decks and does not endorse or recommend commercial products or services. However, the following companies do offer a card deck available for online purchase:
    <p>
        <a href="https://agilestationery.com/" target="_blank">Agile Stationary</a> offer large print decks. They also offer a <a rel="noopener nofollow" href="https://croupier.agilestationery.co.uk/">croupier</a> to help you distribute cards to team members. A small donation is made to the OWASP Foundation for each deck sold.
    </p>
    <p>
        <a href="https://dotnetlab.eu/home-en/" target="_blank">DotNET lab</a> sell a smaller printed deck from an earlier version of the deck (v1.22). This deck has QR codes that works together with their online references. In collaboration with DotNET lab we will soon open a web shop that will be available from this site, so stay tuned!
    </p>
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