<script lang="ts">
    import type { PageMetadata } from "$lib/types/metadata.js";

    interface Props {
        metadata: PageMetadata;
    }

    let { metadata }: Props = $props();
</script>

<svelte:head>
    <title>{metadata.title}</title>
    <link rel="canonical" href="{metadata.canonicalUrl}" />
    <meta name="description" content="{metadata.description}" />
    <meta name="keywords" content="{metadata.keywords}" />
    <!-- Facebook Meta Tags -->
    <meta property="og:url" content="{metadata.canonicalUrl}" />
    <meta property="og:type" content="{metadata.type ?? 'website'}" />
    <meta property="og:title" content="{metadata.title}" />
    <meta property="og:description" content="{metadata.description}" />
    <meta property="og:image" content="{metadata.imageUrl ?? '/images/opengraph.png'}" />
    <!-- Twitter Meta Tags -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta property="twitter:domain" content="cornucopia.owasp.org" />
    <meta property="twitter:url" content="{metadata.canonicalUrl}" />
    <meta name="twitter:title" content="{metadata.title}" />
    <meta name="twitter:description" content="{metadata.description}" />
    <meta name="twitter:image" content="{metadata.imageUrl ?? '/images/opengraph.png'}" />
    <!-- END of Tags -->
</svelte:head>