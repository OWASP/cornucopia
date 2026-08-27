<script lang="ts">
    import { page } from "$app/stores";
    import { readTranslation } from "$lib/stores/stores";
    let t = readTranslation();
</script>

<svelte:head>
    <title>{$page.data.title ?? $t("layout.title")}</title>
    <link rel="canonical" href="{$page.data.url ?? "https://cornucopia.owasp.org"}" />
    <meta name="description" content="{$page.data.description ?? $t("layout.description")}" />
    <!-- Facebook Meta Tags -->
    <meta property="og:url" content="{$page.data.url ?? "https://cornucopia.owasp.org"}" />
    <meta property="og:type" content="{$page.data.ogType ?? "website"}" />
    <meta property="og:title" content="{$page.data.title ?? $t("layout.title")}" />
    <meta property="og:description" content="{$page.data.description ?? $t("layout.description")}" />
    <meta property="og:image" content="/images/opengraph.png" />
    <!-- Twitter Meta Tags -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta property="twitter:domain" content="cornucopia.owasp.org" />
    <meta property="twitter:url" content="{$page.data.url ?? "https://cornucopia.owasp.org"}" />
    <meta name="twitter:title" content="{$page.data.title ?? $t("layout.title")}" />
    <meta name="twitter:description" content="{$page.data.description ?? $t("layout.description")}" />
    <meta name="twitter:image" content="/images/opengraph.png" />
    <!-- END of Tags -->
</svelte:head>