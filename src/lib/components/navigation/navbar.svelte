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

    let links : Link[] = [];
    AddLink(links,$t('about.title'),"/about");
    AddLink(links,$t('printing.title'),"/printing");
    AddLink(links,$t('swags.title'),"/prizes-and-swags");
    AddLink(links,$t('news.title'),"/news");
    AddLink(links,$t('taxonomy.title'),"/taxonomy");
    AddLink(links,$t('cards.title'),"/cards");
    AddLink(links,$t('play.title'),"/how-to-play");
    AddLink(links,$t('home.title'),"/");

    function getMobile(w: number, h: number) {
        mobile = w / h < 1;
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


$: getMobile(width, height);


</script>

<svelte:window bind:innerWidth={width} bind:innerHeight={height} />

<nav>
    <a class="logo" href="/">CORNUCOPIA</a>
    {#if mobile}
        {#if menuOpen}
            <button data-umami-event="mobile-navbar-open-button" in:fade on:click={toggleMenu}><img alt="button to close the menu" src="/icons/close.png"/></button>
        {:else}
            <button data-umami-event="mobile-navbar-close-button" in:fade on:click={toggleMenu}><img alt="button to open the menu" src="/icons/menu.png"/></button>
        {/if}
    {:else}
        <a data-umami-event="desktop-webshop-button" class="link webshop" href="/webshop">{$t('webshop.title')}</a>
        {#each links as link}
            <a data-umami-event="desktop-navbar-{link.name}-button" class="link" href="{link.href}">{link.name}</a>
        {/each}
    {/if}
</nav>

{#if menuOpen}
    <div class="mobile-menu">
        {#each [...links].reverse() as link}
            <button data-umami-event="mobile-navbar-{link.name}-button" class="link-mobile" on:click={()=>{toggleMenu();goto(link.href)}}>{link.name}</button>
        {/each}
        <button data-umami-event="mobile-webshop-button" class="link-mobile" on:click={()=>{window.location.href = '/webshop'}}>Webshop</button>
    </div>
{/if}

<style>
    .webshop
    {
        border: 4px white solid;
        padding : .5rem;
        margin-right: 1.5rem!important;
    }
    .webshop:hover
    {
        text-decoration: none!important;
        background-color: white;
        color:black;
    }

    .link-mobile
    {
        color:var(--white);
        text-decoration: none;
        font-size: 2rem;;
        display: none;
        width : 100%;
        font-family: var(--font-title);
        text-align: center;
        padding-top: 0rem;
        padding-bottom: 0rem;
        border-bottom: 1px rgba(255, 255, 255, 0.203) solid;
    }
    .mobile-menu
    {
        position: fixed;
        width : 100%;
        height : 100%;
        background-color: var(--background);
        z-index: 100;
    }
    button
    {
        background:none;
        border:none;
        float:right;
        margin:1rem;
    }
    img
    {
        width : 3rem;
    }
    .link
    {
        float:right;
        color:white;
        text-decoration: none;
        padding: .5rem;
        font-size: 1.5rem;
        margin-left:.2rem;
        margin-right:.2rem;
        margin-top: 1rem;
        transition: var(--transition);
        font-weight: bold;
    }

    .link:hover
    {
        opacity: 50%;
    }

    .logo
    {
        display:inline-block;
        width : 15rem;
        text-decoration: none;
        margin:0;
        font-size: 2.5rem;
        padding: 1rem;
        font-weight: bold;
        text-decoration: none;
        color:white;
        transition: var(--transition);
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

    .webshop:hover
    {
        opacity: 100%;
        color:var(--background);
        background-color: white;
    }

    @media (max-aspect-ratio: 1/1) 
    {
        .link-mobile
        {
            display: block;
        }

        .link
        {
            display:none;
        }
    }
</style>