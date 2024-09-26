<script>
    import Hero from "$lib/components/hero/hero.svelte";
    import Spacer from "$lib/components/spacer.svelte";
    import TextImage from "$lib/components/textImage.svelte";

    export let data;
</script>


<Hero suits={data.suits}></Hero>
<TextImage src="/images/cornucopia_logo.svg" align="right">
    <h1 id="top">Identify threats</h1>
    <p>
        Owasp Cornucopia is a card game, meant to be played in an agile development context.
        It allows developers to identify and discuss security requirements for their software applications.
        It is an easy way to introduce the practice of threat modeling in a software development team. 
        Playing the card game encourages developers to actively think about the kind of threats that can emerge when creating software. 
        This empowers teams to independently secure their applications while building them. 
        Doing so embraces the shift-left strategy, where security becomes an integrated part of the development cycle.      </p>
    <a href="/how-to-play">Learn how to play ➔</a>
</TextImage>

<TextImage src="/images/github-mark.svg" align="left">
    <h1>Open source</h1>
    <p>
        One of the main advantages of the OWASP Cornucopia card game being open source is that it allows anyone to access and use the game without any licensing fees or restrictions. This encourages widespread adoption and makes it easier for teams to integrate the game into their security practices. Additionally, being open source means that the game is transparent and customizable. Teams can modify the game to suit their specific needs and address the security threats that are most relevant to their applications. They can also contribute back to the game's development by submitting new cards or improvements. Furthermore, open source software tends to have a large and active community of developers who contribute to the codebase and offer support. This can lead to faster bug fixes and updates, ensuring that the game remains relevant and effective in identifying security threats.    
    </p>
    <a href="https://github.com/OWASP/cornucopia">View source on Github ➔</a>
</TextImage>

<TextImage src="/images/cornucopia_logo.svg" align="right">
    <h1>Agile</h1>
    <p>
        The OWASP Cornucopia card game can be effectively integrated into an Agile development process. In Agile, the focus is on delivering working software quickly and continuously improving it based on feedback. The Cornucopia game can be used to identify potential security threats early in the development process, allowing teams to address them before they become major issues. The game can be played during planning sessions, where teams can discuss the security risks associated with each feature and prioritize them accordingly. It can also be used during testing to ensure that all identified risks have been addressed before releasing the software. The game can be played by cross-functional teams, including developers, testers, and security experts, to promote collaboration and shared responsibility for security. The game's flexible and customizable nature also allows teams to tailor it to their specific Agile process and development methodologies. By integrating the Cornucopia game into Agile development, teams can ensure that security is a key consideration throughout the entire software development lifecycle.
    </p>
    <a href="/how-to-play">Learn how to play ➔</a>
</TextImage>
<Spacer></Spacer>

<style>
    h1
    {
        color: var(--background);
        font-weight: bold;
        margin:0;
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
        padding: .5rem;
        border-radius: .5rem;
        transition: var(--transition);
        margin-top: 1rem;
    }

    a:hover
    {
        opacity: 70%;
        transform: translate(1rem,0);
        color: rgb(41, 0, 176);
    }
</style>