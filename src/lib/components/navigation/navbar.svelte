<script lang="ts">
    import { goto } from "$app/navigation";
    import { fade } from "svelte/transition";
    import { AddLink, type Link } from "./utils";
    import {readTranslation} from "$lib/stores/stores";
    let t = readTranslation();
    let width: number;
    let height: number;
    let mobile: boolean = false;
    let menuOpen : boolean = false;
    let subMenuOpen : boolean = false;

    let mainMenu : Link[] = [];
    AddLink(mainMenu,$t('home.title'),"/");
    AddLink(mainMenu,$t('play.title'),"/how-to-play");
    AddLink(mainMenu,$t('cards.title'),"/cards");
    AddLink(mainMenu,$t('taxonomy.title'),"/taxonomy");
    AddLink(mainMenu,$t('news.title'),"/news");
    AddLink(mainMenu,$t('about.title'),"/about");
    
    let subMenu : Link[] = [];
    AddLink(subMenu,$t('webshop.title'),"/webshop");
    AddLink(subMenu,$t('printing.title'),"/printing");
    AddLink(subMenu,$t('swags.title'),"/swags");

    function getMobile(w: number, h: number) {
        mobile = w / h < 1.8;
    }


    function toggleMenu()
    {
        menuOpen = !menuOpen;
        if(menuOpen)
        {
             document.body.style["overflow"] = "hidden"
        }
        else
        {
            document.body.style["overflow"] = "auto"
        }
    }

    function toggleSubMenu(e)
    {
        let menu = document.getElementsByClassName('sub-menu');
        subMenuOpen = !subMenuOpen;
        if(subMenuOpen)
        {
            for (const item of menu) item.style.display = 'none';
        }
        else
        {
            for (const item of menu) item.style.display = 'block';
        }
    }


$: getMobile(width, height);


</script>

<svelte:window bind:innerWidth={width} bind:innerHeight={height} />
<header id="menu">
    <nav>
        <a class="logo" href="/"><div><span class="desktop">OWASP </span><span class="desktop mobile">Cornucopia</span></div></a>
        <ul>
        {#if mobile}
            {#if menuOpen}
                <button data-umami-event="mobile-navbar-open-button" in:fade on:click={toggleMenu}><img alt="button to close the menu" src="/icons/close.png"/></button>
            {:else}
                <button data-umami-event="mobile-navbar-close-button" in:fade on:click={toggleMenu}><img alt="button to open the menu" src="/icons/menu.png"/></button>
            {/if}
        {:else}
        
        
        {#each mainMenu as link}
            <li class="general-menu">
                <a data-umami-event="desktop-navbar-{link.name}-button" class="link" href="{link.href}"><div>{link.name}</div></a>
            </li>
        {/each}
            <li>
                <a data-umami-event="desktop-webshop-button" in:fade on:click={toggleSubMenu} class="link get-game" href="#menu"><div>{$t('getthegame.title')}</div></a>
                <div>
                    <ul class="sub-menu">
                {#each subMenu as link}
                        <li><a data-umami-event="desktop-navbar-{link.name}-button" class="link sub-menu" href="{link.href}"><div>{link.name}</div></a></li>
                {/each}
                    </ul>
                </div>
            </li>
        {/if}
        </ul>
    </nav>
</header>
{#if menuOpen}
    <div class="mobile-menu">
        {#each [...mainMenu].reverse() as link}
            <button data-umami-event="mobile-navbar-{link.name}-button" class="link-mobile" on:click={()=>{toggleMenu();goto(link.href)}}><span>{link.name}</span></button>
        {/each}
        {#each [...subMenu].reverse() as link}
            <button data-umami-event="mobile-navbar-{link.name}-button" class="link-mobile" on:click={()=>{toggleMenu();goto(link.href)}}><span>{link.name}</span></button>
        {/each}
    </div>
{/if}

<style>
    * {margin: 0;outline: none;-webkit-box-sizing: border-box;-moz-box-sizing: border-box;box-sizing: border-box;}
    *:after, *:before { -webkit-box-sizing: border-box;-moz-box-sizing: border-box;box-sizing: border-box;}
    nav {  display: block;}

    header {
		display: block;
		position: fixed;
		width: 100%;
		z-index: 1000;
	}
	
	header > nav > ul {
		display: flex;
		flex-wrap: wrap;
		justify-content: flex-start;
		list-style: none;
        float: right;
	}
	
    header > nav > ul > li {
        flex: 0 1 auto;
        margin: 0;
        position: relative;
        transition: all linear 0.1s;	
    }
    
    header > nav > ul > li a + div {
        border-radius: 0 0 2px 2px;
        display: none;
        font-size: 1vw;
        position: absolute;
        top: 4.3rem;
        width: 14vw;
    }
			
    header > nav > ul > li:hover a + div {
        display: block;
    }

    ul.sub-menu > li > a > div {
        padding: 0.5vw;
    }
    
    header > nav > ul > li a + div > ul {
        list-style-type: none;
        height: 13.5rem;
        border-radius: 0 0 4px 4px;
        background-color: rgb(31, 41, 55);
        border: 1px white solid;
        
    }
				
    header > nav > ul > li a + div > ul > li {
        margin: 0;
        display: flex;
    }
					
    header > nav > ul > li a + div > ul > li > a {
        letter-spacing: 0.15vw;
        padding: 0.25vw 1.5vw;
    }
	
    header > nav > ul > li > a {
        align-items: flex-start;
        display: flex;
        max-width: 15vw;
        padding: 1vw 1.5vw;
    }


    .get-game {
        display: flex;
        text-align: top;
        background-color: rgb(31, 41, 55);
    }
    

    .link-mobile
    {
        color:var(--white);
        text-decoration: none;
        font-size: 2rem;
        width : 100%;
        font-family: var(--font-title);
        text-align: center;
        padding-top: 0;
        padding-bottom: 0;
        border-bottom: 1px rgba(255, 255, 255, 0.203) solid;
    }
    .link-mobile:hover > span {
        opacity: 50%;
    }
    .mobile-menu
    {
        position: fixed;
        width : 100%;
        top: 5rem;
        height : 25rem;
        background-color: var(--background);
        z-index: 100;
    }
    button
    {
        background: none;
        border: none;
        float: right;
        padding-left: 1vw;
        padding-top: 0.5rem;
    }
    img
    {
        width : 4rem;
    }
    .link
    {
        float:right;
        color:#ffffff;
        text-decoration: none;
        padding-left: .4vw;
        padding-right: .4vw;
        padding-top: .5rem;
        font-size: 1.5vw;
        margin-top: 1rem;
        transition: var(--transition);
        font-weight: bold;
    }
    .general-menu
    {
        padding-top: 0.25rem;
    }

    .get-game
    {
        border: 3px white solid;
        padding : .5rem;
        margin-right: 1.5rem!important;
        min-width: 14vw;
    }
    .get-game:hover
    {
        text-decoration: none!important;
        background-color: white;
        color:black;
    }

    ul.sub-menu {
        padding-inline-start: 0;
    }

    a.sub-menu {
        float: left;
        font-size: 1.3vw;
        margin-left: 0.2vw;
        padding: 0;
        
    }
    a.sub-menu:hover {
        opacity: 100%;
        
        background-color: white;
        color: rgb(31, 41, 55);
    }

    .link:hover
    {
        opacity: 50%;
    }

    .logo {
        display:inline-block;
        margin-top: 0.4rem;
        width : 36vw;
        max-width: 36vw;
        font-size: 3.1vw;
        padding: 1rem;
        font-weight: bold;
        text-decoration: none;
        color:white;
        transition: var(--transition);
        text-transform: uppercase;
    }

    header > nav > .logo > div {
        bottom: 1vw;
        position: relative;
        min-width: 18rem;
    }


    .logo:hover
    {
        opacity: 50%;
    }
    
    nav
    {
        width : 100%;
        height : 5rem;
        background-color: rgb(31, 41, 55);
        border-bottom: 1px var(--white) solid;
    }

    @media (max-aspect-ratio: 1/1) 
    {
        .link-mobile
        {
            display: none;
        }
        .mobile-menu 
        {
            display: none;
        }

        .link
        {
            display: block;
        }
        .desktop
        {
            display: none;
        }
        .mobile
        {
            display: inline;
            font-size: 8vw;
        }
        .logo {
            margin-top: 0rem;
        }
    }
</style>