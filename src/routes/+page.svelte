<script lang="ts">
    import Hero from "$lib/components/hero/hero.svelte";
    import Spacer from "$lib/components/spacer.svelte";
    import TextImage from "$lib/components/textImage.svelte";
    import { readLang } from "$lib/stores/stores.js";
    import type { Suit } from "../domain/suit/suit.js";

    export let data;
    const lang = readLang();
    let suits = data.suits.get(`webapp-${$lang}`);

    if (suits == undefined) {
        suits = data.suits.get('webapp-en') as Suit[];
    }
</script>


<Hero cards={data.cards} {suits} mapping={data.mappingData.get('webapp')}></Hero>
<TextImage src="/images/cornucopia_logo_in_devs_we_trust.svg" align="right">
    <h1 id="top">Introduction</h1>
    <p>
        The idea behind Cornucopia is to help development teams, especially those using Agile methodologies, to identify application security requirements and develop security-based user stories.
    </p>
    <p>
        OWASP Cornucopia is an easy way to introduce the practice of threat modeling in a software development team. 
        Playing the card game encourages the development team to actively think about the kind of threats that can emerge when creating software. 
        This empowers teams to independently secure their applications while building them. 
        Doing so embraces the shift-left strategy, where security becomes an integrated part of the development cycle.</p>
    <a href="/about" class="internal-links">➔ Read more</a>
</TextImage>
<TextImage src="/images/cornucopia_logo_mobile_edition.svg" align="left">
    <h1 id="top">How to start</h1>
    <p>To start using Cornucopia:</p>
    <ol>
        <li><b>Either</b> Obtain or buy a pre-printed deck of cards;</li>
        <li><b>Or:</b> Download the free Adobe Illustrator files and get them professionally printed (see: <a href="/printing">printing instructions</a>);</li>
        <li><b>Or:</b> Play the game online at <a rel="noopener" href="https://copi.owasp.org">copi.owasp.org</a>.</li>
        <li>Identify an application, module or component to assess.</li>
        <li>Invite business owners, architects, developers, testers along for a card game.</li>
        <li>Get those infosec folk to provide chocolate, pizza, beer, flowers or all four as prizes.</li>
        <li>Select a portion of the deck to start with.</li>
        <li><a href="/how-to-play">Play the game</a> to discuss & document security requirements (and to win rounds).</li>
        <li>Remember, to have fun!</li>
    </ol>
    <a href="/how-to-play" class="internal-links">➔ How to play</a>
</TextImage>
<TextImage src="/images/opensource.png" align="right">
    <h1>Open source</h1>
    <p>
        There are a large number of source design files for the cards themselves in various languages and formats.
        These design files together with the source code to generate the Word document, PDFs and InDesign files for printing are maintained in our <a rel="noopener" href="https://github.com/OWASP/cornucopia/releases/tag/v2.0.0">Github repository</a>.
    </p>
    <p>
        One of the main advantages of the OWASP Cornucopia card game being open source is that it allows anyone to access and use the game without any licensing fees or restrictions. This encourages widespread adoption and makes it easier for teams to integrate the game into their security practices. Additionally, being open source means that the game is transparent and customizable. Teams can modify the game to suit their specific needs and address the security threats that are most relevant to their applications. They can also contribute back to the game's development by submitting new cards or improvements. Furthermore, open source software tends to have a large and active community of developers who contribute to the codebase and offer support. This can lead to faster bug fixes and updates, ensuring that the game remains relevant and effective in identifying security threats.
    </p>
    <a class="internal-links" href="https://github.com/OWASP/cornucopia">View source on Github ➔</a>
</TextImage>
<Spacer></Spacer>
<style>
    h1
    {
        color: var(--background);
        font-weight: bold;
        margin:0;
    }

    a,p,ol
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
</style>