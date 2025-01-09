<script lang="ts">
    import { goto } from "$app/navigation";
    import { fade } from "svelte/transition";
    import { AddLink, type Link } from "./utils";
    import {readTranslation} from "$lib/stores/stores";
    let t = readTranslation();
    let width: number = $state();
    let height: number = $state();

    let mainMenu : Link[] = [];
    AddLink(mainMenu,$t('home.title'),"/");
    AddLink(mainMenu,$t('play.title'),"/how-to-play");
    AddLink(mainMenu,$t('cards.title'),"/cards");
    AddLink(mainMenu,$t('taxonomy.title'),"/taxonomy");
    AddLink(mainMenu,$t('news.title'),"/news");
    AddLink(mainMenu,$t('about.title'),"/about");
    
    let subMenu : Link[] = [];
    AddLink(subMenu,$t('source.title'),"/source");
    AddLink(subMenu,$t('printing.title'),"/printing");
    AddLink(subMenu,$t('swags.title'),"/swags");
    AddLink(subMenu,$t('webshop.title'),"/webshop");

    function toggleMenu()
    {
        let menuButton = document.getElementsByClassName('mobile-nav-button');
        for (const item of menuButton) item.checked = false;
    }

</script>

<svelte:window bind:innerWidth={width} bind:innerHeight={height} />
<header id="menu">
    <nav>
        <div id="mobile-menu">
            <input class="mobile-nav-button" in:fade type="checkbox" />
            <ul class="mobile-menu">
                <li>
                    <ul>
                        {#each [...mainMenu].reverse() as link}
                        <li>
                            <button class="link-mobile" onclick={()=>{toggleMenu();goto(link.href)}}><span>{link.name}</span></button>
                        </li>
                        {/each}
                        {#each [...subMenu].reverse() as link}
                        <li>
                            <button class="link-mobile" onclick={()=>{toggleMenu();goto(link.href)}}><span>{link.name}</span></button>
                        </li>
                        {/each}
                    </ul>
                </li>
            </ul>
        </div>
        <ul class="desktop-menu">
            {#each mainMenu as link}
                <li class="general-menu">
                    <a class="link" href="{link.href}"><div>{link.name}</div></a>
                </li>
            {/each}
                <li class="sub-menu">
                    <a in:fade class="link get-game" href="#menu"><div>{$t('getthegame.title')}</div></a>
                    <div>
                        <ul class="sub-menu">
                        {#each subMenu as link}
                             <li><a class="link sub-menu" href="{link.href}"><div>{link.name}</div></a></li>
                        {/each}
                        </ul>
                    </div>
                </li>
            </ul>
        <a class="logo" href="/"><div><span class="desktop">OWASP</span>&nbsp;<span class="desktop mobile">Cornucopia</span></div></a>
        
    </nav>
</header>

<style>
    * {margin: 0;outline: none;padding-inline-start: 0;-webkit-box-sizing: border-box;-moz-box-sizing: border-box;box-sizing: border-box;}
    *:after, *:before { -webkit-box-sizing: border-box;-moz-box-sizing: border-box;box-sizing: border-box;}
    nav {  display: block;}

    header {
        
		position: sticky;
		width: 100%;
		z-index: 100;
	}

    header > nav {
        display: flex;
        flex-direction: row-reverse;
        justify-content: flex-end;
        justify-content: space-between;
    }
	
	header > nav > ul {
        display: flex;
		list-style: none;
        padding: 0;
	}
	
    header > nav > ul > li {
        flex: 0 1 auto;
        margin: 0;
        position: relative;
        transition: all linear 0.1s;
        white-space: nowrap;	
    }
    
    header > nav > ul > li a + div {
        border-radius: 0 0 2px 2px;
        font-size: 1vw;
        top: 3.2rem;
        width: 14vw;
    }
			
    header > nav > ul > li:hover a + div {
        display: block;
    }

    ul.sub-menu > li > a > div {
        padding: 0.5vw;
    }
    
    header > nav > ul > li a + div > ul {
        display: flex;
        list-style-type: none;
        height: 17.5vw;
        border-radius: 0 0 2px 2px;
        background-color: rgb(31, 41, 55);
        border: 2px white solid;
        
    }
				
    header > nav > ul > li a + div > ul > li {
        margin: 0;
        flex-direction: column;
    }
					
    header > nav > ul > li a + div > ul > li > a {
        letter-spacing: 0.15vw;
        padding: 0.25vw 1.5vw;
    }
	
    header > nav > ul > li > a {
        max-width: 15vw;
        padding: 1vw 1.5vw;
    }


    .get-game {
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

    .mobile-nav-button {
        content: url('/icons/menu.png');
        appearance: none;
        display: inline-flex;
        width: 4.1rem;
        height: 4.1rem;
        align-self: flex-end;

    }

    .mobile-nav-button:checked {
        content: url('/icons/close.png');

    }

    .mobile-nav-button:hover {
        opacity: 50%;
    }

    #mobile-menu
    {
        display: none;
        flex-direction: column;
        justify-content: flex-start;
        
    }
    .mobile-menu {
        width : 100%;
        margin-top: 0.9rem;
        height : 30rem;
        background-color: var(--background);
        z-index: 100;
        border-radius: 0 0 10px 10px;
        padding-bottom: 1rem;
        padding: 0 1rem 1rem;
        
    }
    

    input + ul.mobile-menu
    {
        display: none;
        -webkit-animation: fadeOutFromNone 0.5s ease-out;
        -moz-animation: fadeOutFromNone 0.5s ease-out;
        -o-animation: fadeOutFromNone 0.5s ease-out;
        animation: fadeOutFromNone 0.5s ease-out;
    }

    button
    {
        background: none;
        border: none;
        float: right;
        padding-left: 1vw;
        padding-top: 0.5rem;
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
        border: 2px white solid;
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

    .get-game + div
    {
        display: none;
    }

    .get-game:hover + div
    {
        display: block;
    }

    ul.sub-menu {
        padding-inline-start: 0;
        flex-direction: column;
    }

    a.sub-menu {
        font-size: 1.3vw;
        margin-left: 0.2vw;
        padding: 0;
        width: 100%;
        border-radius: 0rem;
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
        margin-top: 0.4rem;
        width : 36vw;
        max-width: 36vw;
        font-size: 3vw;
        padding: 1rem;
        font-weight: bold;
        text-decoration: none;
        color:white;
        transition: var(--transition);
        text-transform: uppercase;
        white-space: pre;
        overflow: hidden;
        
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
        .desktop-menu {
            display: none;
        }

        #mobile-menu
        {
            display: flex;
        }

        input:checked + ul.mobile-menu
        {
            display: flex;

            -webkit-animation: fadeInFromNone 0.5s ease-out;
            -moz-animation: fadeInFromNone 0.5s ease-out;
            -o-animation: fadeInFromNone 0.5s ease-out;
            animation: fadeInFromNone 0.5s ease-out;
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
            overflow: visible;
        }

        @-webkit-keyframes fadeInFromNone {
            0% {
                display: none;
                opacity: 0;
            }

            1% {
                display: flex;
                opacity: 0;
            }

            100% {
                display: flex;
                opacity: 1;
            }
        }

        @-moz-keyframes fadeInFromNone {
            0% {
                display: none;
                opacity: 0;
            }

            1% {
                display: flex;
                opacity: 0;
            }

            100% {
                display: flex;
                opacity: 1;
            }
        }

        @-o-keyframes fadeInFromNone {
            0% {
                display: none;
                opacity: 0;
            }

            1% {
                display: flex;
                opacity: 0;
            }

            100% {
                display: flex;
                opacity: 1;
            }
        }

        @keyframes fadeInFromNone {
            0% {
                display: none;
                opacity: 0;
            }

            1% {
                display: flex;
                opacity: 0;
            }

        }
    }




</style>