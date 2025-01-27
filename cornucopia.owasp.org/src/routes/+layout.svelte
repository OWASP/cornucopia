<script lang="ts">
    import 'normalize.css';
    import { browser } from "$app/environment";
    import { page } from "$app/stores";
    import Breadcrumbs from "$lib/components/breadcrumbs.svelte";
    import Footer from "$lib/components/footer.svelte";
    import Metadata from "$lib/components/metadata.svelte";
    import Navbar from "$lib/components/navigation/navbar.svelte";
    import {updateTranslation, updateLang} from "$lib/stores/stores";    
    interface Props {
        data: any;
        children?: import('svelte').Snippet;
    }

    let { data, children }: Props = $props();
    updateTranslation(data.translation, data.fallbackTranslation);
    updateLang(data.lang);
    
    let content = data.content.get(data.lang) || data.content.get('en');

    function getFullWidthPages(path : string)
    {
        // Add exceptions for page that need to be shown full page width
        if(path == '/')
            return true;
        return false;
    }

    // intercept innerHTML invocation and remove style before div is added to dom
    $effect(() => {
    if (browser) {
        const originalInnerHTML = Object.getOwnPropertyDescriptor(Element.prototype, 'innerHTML');
        
        Object.defineProperty(Element.prototype, 'innerHTML', {
        set(value: string) {
            if (value.includes('id="svelte-announcer"')) {
            const safeValue = value.replace(/style=".*?"/i, '');
            originalInnerHTML?.set?.call(this, safeValue);
            } else {
            originalInnerHTML?.set?.call(this, value);
            }
        }
        });
    }
    });

    // add styles back in non-CSP violating way
    $effect(() => {
    if (document) {
        const observer = new MutationObserver((mutations) => {
        for (const mutation of mutations) {
            for (const node of mutation.addedNodes) {
            if (node instanceof HTMLDivElement && node.id === 'svelte-announcer') {
                node.style.position = 'absolute';
                node.style.left = '0';
                node.style.top = '0';
                node.style.clip = 'rect(0 0 0 0)';
                node.style.clipPath = 'inset(50%)';
                node.style.overflow = 'hidden';
                node.style.whiteSpace = 'nowrap';
                node.style.width = '1px';
                node.style.height = '1px';
            }
            }
        }
        });

        observer.observe(document, {
        childList: true,
        subtree: true
        });
    }
    });
</script>

<Metadata></Metadata>

<div class="page">
    <Navbar></Navbar>
    <div class="slot-container" class:wide={getFullWidthPages($page.url.pathname)}>
        <Breadcrumbs></Breadcrumbs>
        {@render children?.()}
    </div>
    <Footer timestamp={data.timestamp} {content}></Footer>
</div>

<style>
    .page
    {
        background-color:var(--background-color);
    }

    .wide
    {
        width: 100% !important;
    }

    .slot-container
    {
        width: 60%;
        min-height: 100vh;
        margin : auto;
        padding-bottom: 1rem;
    }

    @media (max-aspect-ratio: 1/1)
    {
        .slot-container
        {
            width: 100%;
        }
    }
</style>