<script lang="ts">
    import { goto } from "$app/navigation";
    import { resolve } from "$app/paths";
    import { page } from "$app/stores";
    import { AddLink, type Link } from "./utils";
    import { readTranslation } from "$lib/stores/stores";

    let t = readTranslation();

    let mainMenu: Link[] = [];
    AddLink(mainMenu, $t("home.title"), "/");
    AddLink(mainMenu, $t("play.title"), "/how-to-play");
    AddLink(mainMenu, $t("cards.title"), "/cards");
    AddLink(mainMenu, $t("taxonomy.title"), "/taxonomy");
    AddLink(mainMenu, $t("news.title"), "/news");
    AddLink(mainMenu, $t("about.title"), "/about");
    AddLink(mainMenu, $t("tribute.title"), "/tribute");

    let subMenu: Link[] = [];
    AddLink(subMenu, $t("source.title"), "/source");
    AddLink(subMenu, $t("printing.title"), "/printing");
    AddLink(subMenu, $t("copi.title"), "/copi");
    AddLink(subMenu, $t("swags.title"), "/swags");
    AddLink(subMenu, $t("webshop.title"), "/webshop");

    function closeMenu() {
        const toggle = document.getElementById("menu-toggle") as HTMLInputElement | null;
        if (toggle) toggle.checked = false;
    }

    function navTo(href: string) {
        closeMenu();
        goto(resolve(href));
    }

    function isActive(href: string): boolean {
        const path = $page.url.pathname;
        if (href === "/") return path === "/";
        return path === href || path.startsWith(href + "/");
    }
</script>

<header id="menu">
    <input type="checkbox" id="menu-toggle" class="menu-toggle-input" aria-hidden="true" />

    <nav class="top-nav" aria-label="Main navigation">
        <a class="logo" href={resolve("/")} aria-label="OWASP Cornucopia Home">
            <img
                src="/images/cornucopia_logo_white.svg"
                alt="OWASP Cornucopia"
                class="logo-img"
            />
        </a>

        <ul class="desktop-menu" role="list">
            {#each mainMenu as link (link.href)}
                <li>
                    <a
                        class="nav-link"
                        class:active={isActive(link.href)}
                        href={resolve(link.href)}
                        aria-current={isActive(link.href) ? "page" : undefined}
                    >
                        {link.name}
                    </a>
                </li>
            {/each}
        </ul>

        <div class="nav-right">
            <div class="dropdown-wrap desktop-only">
                <input type="checkbox" id="sub-toggle" class="sub-toggle-input" aria-hidden="true" />
                <label for="sub-toggle" class="nav-link get-game-btn">
                    {$t("getthegame.title")}
                </label>
                <ul class="dropdown-menu" role="menu">
                    {#each subMenu as link (link.href)}
                        <li role="none">
                            <a class="dropdown-item" href={resolve(link.href)} role="menuitem">
                                {link.name}
                            </a>
                        </li>
                    {/each}
                </ul>
            </div>
            <a class="cta-btn desktop-only" href="https://copi.owasp.org/">Play Online</a>
            <label for="menu-toggle" class="hamburger mobile-only" aria-label="Toggle menu">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </label>
        </div>
    </nav>

    <label for="menu-toggle" class="backdrop" aria-hidden="true"></label>

    <nav id="mobile-drawer" class="mobile-drawer" aria-label="Mobile navigation">
        <div class="drawer-header">
            <img
                src="/images/cornucopia_logo_white.svg"
                alt=""
                class="drawer-logo"
            />
            <span class="drawer-title">Menu</span>
            <label for="menu-toggle" class="close-btn" aria-label="Close menu">X</label>
        </div>

        <ul class="drawer-links" role="list">
            {#each mainMenu as link (link.href)}
                <li>
                    <button
                        type="button"
                        class="drawer-link"
                        class:active={isActive(link.href)}
                        onclick={() => navTo(link.href)}
                    >
                        {link.name}
                    </button>
                </li>
            {/each}
        </ul>

        <div class="drawer-divider" aria-hidden="true"></div>
        <div class="drawer-section-label">{$t("getthegame.title")}</div>

        <ul class="drawer-links" role="list">
            {#each subMenu as link (link.href)}
                <li>
                    <button
                        type="button"
                        class="drawer-link sub"
                        onclick={() => navTo(link.href)}
                    >
                        {link.name}
                    </button>
                </li>
            {/each}
        </ul>

        <div class="drawer-cta">
            <a class="cta-btn drawer-cta-btn" href="https://copi.owasp.org/" onclick={closeMenu}>
                Play Online
            </a>
        </div>
    </nav>
</header>

<style>
    header {
        position: sticky;
        top: 0;
        width: 100%;
        z-index: 100;
        background-color: rgb(31, 41, 55);
        border-bottom: 1px solid #e85d04;
    }

    .menu-toggle-input,
    .sub-toggle-input {
        display: none;
    }

    .top-nav {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        height: 5rem;
        padding: 0 1.5rem;
        gap: 1rem;
    }

    .logo {
        overflow: visible;
        display: flex;
        align-items: center;
        text-decoration: none;
        flex-shrink: 0;
        transition: opacity 0.15s;
    }

    .logo:hover {
        opacity: 0.7;
    }

    .logo-img {
        height: 4rem;
        width: auto;
        max-width: 9rem;
        display: block;
    }

    .desktop-menu {
        display: flex;
        align-items: center;
        list-style: none;
        margin: 0;
        padding: 0;
        gap: 0.15rem;
        flex: 1;
        justify-content: center;
    }

    .nav-link {
        color: #fff;
        text-decoration: none;
        font-size: 1.5vw;
        font-weight: bold;
        padding: 0.5rem 0.75rem;
        transition: opacity 0.15s;
        white-space: nowrap;
        cursor: pointer;
    }

    .nav-link:hover {
        opacity: 0.5;
    }

    .nav-link.active {
        color: #fb923c;
    }

    .get-game-btn {
        background: #e85d04;
        color: #fff;
        border-radius: 4px;
        padding: 0.45rem 1rem;
        font-size: 0.9rem;
        border: none;
        margin-left: 0.25rem;
    }

    .get-game-btn:hover {
        background: #c2410c;
        opacity: 1;
    }

    .dropdown-wrap {
        position: relative;
    }

    .dropdown-menu {
        display: none;
        position: absolute;
        top: calc(100% + 0.25rem);
        left: 0;
        list-style: none;
        margin: 0;
        padding: 0.25rem 0;
        background: rgb(31, 41, 55);
        border: 2px solid #e85d04;
        border-radius: 0 0 4px 4px;
        min-width: 100%;
        z-index: 110;
    }

    .dropdown-wrap:hover .dropdown-menu {
        display: block;
    }

    .dropdown-item {
        display: block;
        color: #fff;
        text-decoration: none;
        font-size: 0.95rem;
        font-weight: bold;
        padding: 0.4rem 1.25rem;
        transition: background 0.15s;
        white-space: nowrap;
    }

    .dropdown-item:hover {
        background: #fff;
        color: rgb(31, 41, 55);
    }

    .nav-right {
        margin-left: auto;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        flex-shrink: 0;
    }

    .cta-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: #e85d04;
        color: #fff;
        text-decoration: none;
        font-weight: bold;
        border-radius: 4px;
        transition: background 0.15s, opacity 0.15s;
        white-space: nowrap;
    }

    .cta-btn:hover {
        background: #c2410c;
    }

    .desktop-only.cta-btn {
        font-size: 0.9rem;
        padding: 0.45rem 1rem;
    }

    .hamburger {
        display: none;
        flex-direction: column;
        justify-content: center;
        gap: 5px;
        width: 2.5rem;
        height: 2.5rem;
        cursor: pointer;
        padding: 0.25rem;
    }

    .bar {
        display: block;
        width: 100%;
        height: 3px;
        background: #fff;
        border-radius: 2px;
        transition: opacity 0.15s;
    }

    .hamburger:hover .bar {
        opacity: 0.6;
    }

    .backdrop {
        display: none;
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.5);
        z-index: 200;
        cursor: pointer;
    }

    .menu-toggle-input:checked ~ .backdrop {
        display: block;
    }

    .mobile-drawer {
        position: fixed;
        top: 0;
        left: 0;
        display: flex;
        flex-direction: column;
        width: min(300px, 82vw);
        height: 100dvh;
        background: #141c2a;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        z-index: 300;
        overflow-y: auto;
        overflow-x: hidden;
        padding-bottom: 0.75rem;
        transform: translateX(-100%);
        transition: transform 0.25s ease;
        box-sizing: border-box;
    }

    .menu-toggle-input:checked ~ .mobile-drawer {
        transform: translateX(0);
    }

    .drawer-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        flex-shrink: 0;
        padding: 1rem 1rem 0.75rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .drawer-logo {
        height: 1.75rem;
        width: auto;
        flex-shrink: 0;
    }

    .drawer-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #fff;
        flex: 1;
    }

    .close-btn {
        color: rgba(255, 255, 255, 0.5);
        font-size: 1.1rem;
        cursor: pointer;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        min-width: 44px;
        min-height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }

    .close-btn:hover {
        color: #fff;
        background: rgba(255, 255, 255, 0.08);
    }

    .drawer-links {
        list-style: none;
        margin: 0;
        padding: 0.35rem 0;
    }

    .drawer-links li {
        margin: 0;
        padding: 0;
    }

    .drawer-link {
        display: block;
        width: 100%;
        box-sizing: border-box;
        text-align: left;
        background: none;
        border: none;
        color: rgba(255, 255, 255, 0.75);
        font-size: 1.05rem;
        font-weight: 600;
        padding: 0.55rem 1.25rem;
        cursor: pointer;
        transition: background 0.15s, color 0.15s;
        line-height: 1.3;
        white-space: normal;
        word-break: normal;
    }

    .drawer-link:hover {
        background: rgba(255, 255, 255, 0.06);
        color: #fff;
    }

    .drawer-link.active {
        color: #fb923c;
        background: rgba(232, 93, 4, 0.12);
        border-left: 3px solid #e85d04;
        padding-left: calc(1.25rem - 3px);
    }

    .drawer-link.sub {
        font-size: 0.9rem;
        font-weight: 400;
        padding: 0.45rem 1.25rem 0.45rem 1.5rem;
        color: rgba(255, 255, 255, 0.55);
    }

    .drawer-divider {
        height: 1px;
        background: rgba(255, 255, 255, 0.08);
        margin: 0.2rem 0;
        flex-shrink: 0;
    }

    .drawer-section-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: rgba(255, 255, 255, 0.35);
        padding: 0.45rem 1.25rem 0.15rem;
        font-weight: 600;
        flex-shrink: 0;
    }

    .drawer-cta {
        padding: 0.75rem 1.25rem 0.75rem 1.25rem;
        margin-top: auto;
        flex-shrink: 0;
    }

    .drawer-cta-btn {
        width: 100%;
        font-size: 0.85rem;
        padding: 0.55rem 1rem;
        border-radius: 4px;
        box-sizing: border-box;
    }

    .desktop-only {
        display: flex;
    }

    .mobile-only {
        display: none;
    }

    @media (max-width: 900px) {
        .top-nav {
            padding: 0 1rem;
        }

        .logo-img {
            height: 4rem;
            width: auto;
            max-width: 9rem;
        }

        .desktop-menu,
        .desktop-only {
            display: none;
        }

        .mobile-only {
            display: flex;
        }
    }

    @media (min-width: 901px) and (max-width: 1024px) {
        .nav-link {
            font-size: 0.78rem;
            padding: 0.4rem 0.5rem;
        }

        .dropdown-item {
        display: block;
        color: #fff;
        text-decoration: none;
        font-size: 0.95rem;
        font-weight: bold;
        padding: 0.4rem 1.25rem;
        transition: background 0.15s;
        white-space: nowrap;
    }
    }
</style>
