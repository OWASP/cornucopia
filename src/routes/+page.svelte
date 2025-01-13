<script lang="ts">
    import Hero from "$lib/components/hero/hero.svelte";
    import Spacer from "$lib/components/spacer.svelte";
    import TextImage from "$lib/components/textImage.svelte";
    import { readLang } from "$lib/stores/stores.js";
    import type { Suit } from "../domain/suit/suit.js";
    import {readTranslation} from "$lib/stores/stores";

    interface Props {
        data: any;
    }

    let { data }: Props = $props();

    let t = readTranslation();
    const lang = readLang();
    let suits = $state(data.suits.get(`webapp-${$lang}`));

    if ((() => suits)() == undefined) {
        suits = data.suits.get('webapp-en') as Suit[];
    }
</script>


<Hero cards={data.cards} {suits} mapping={data.mappingData.get('webapp')}></Hero>
<TextImage src="/images/cornucopia_logo_in_devs_we_trust.svg" align="right">
    <span id="top">{$t('home.h1.1')}</span>
    <p>
        {$t('home.p1')}
    </p>
    <p>
        {$t('home.p2')}
    </p>
    <a href="/about" class="internal-links">➔ {$t('home.a1')}</a>
</TextImage>
<TextImage src="/images/cornucopia_logo_mobile_edition.svg" align="left">

    <span id="top">{$t('home.h1.2')}</span>
    <p>{$t('home.p3')}</p>
    <ol>
        <li>{@html $t('home.ol.li1')}</li>
        <li>{@html $t('home.ol.li2')}<a href="/printing">{$t('home.ol.li2a')}</a>);</li>
        <li>{@html $t('home.ol.li3')}<a rel="noopener" href="https://copi.owasp.org">copi.owasp.org</a>.</li>
        <li>{$t('home.ol.li4')}</li>
        <li>{$t('home.ol.li5')}</li>
        <li>{$t('home.ol.li6')}</li>
        <li>{$t('home.ol.li7')}</li>
        <li><a href="/how-to-play">{$t('home.ol.li8a')}</a>{$t('home.ol.li8')}</li>
        <li>{$t('home.ol.li9')}</li>
    </ol>
    <a href="/how-to-play" class="internal-links">➔ {$t('home.a2')}</a>
</TextImage>
<TextImage src="/images/opensource.png" align="right">
    <span>{$t('home.h1.3')}</span>
    <p>{$t('home.p4.1')}<a rel="noopener" href="https://github.com/OWASP/cornucopia/releases/tag/v2.0.0">{$t('home.p4.2')}</a>.
    </p>
    <p>{$t('home.p5')}</p>
    <a class="internal-links" rel="noopener" href="https://github.com/OWASP/cornucopia">{$t('home.a3')} ➔</a>
</TextImage>
<Spacer></Spacer>
<style>
    span
    {
        display: block;
        color: var(--background);
        font-weight: bold;
        margin:0;
        font-size: 3rem
    }
    

    a,p,ol
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

    a.internal-links
    {
        display: inline-block;
        text-decoration: none;
        font-weight: bold;
        color:var(--background);
        padding: .5rem;
        border-radius: .5rem;
        transition: var(--transition);
        margin-top: 1rem;
    }

    a.internal-links:hover
    {
        opacity: 70%;
        transform: translate(1rem,0);
        color: rgb(41, 0, 176);
    }

    @media (max-aspect-ratio: 1/1) 
    {
        
    }
</style>