<script>
    import { readTranslation } from "$lib/stores/stores";
    let t = readTranslation();
</script>
<svelte:head>
    <meta name="description" content="undefined">
    <!-- Facebook Meta Tags -->
    <meta property="og:url" content="https://cornucopia.owasp.org/">
    <meta property="og:type" content="website">
    <meta property="og:title" content="OWASP Cornucopia">
    <meta property="og:description" content="{$t('layout.description')}">
    <meta property="og:image" content="/images/opengraph.png">

    <!-- Twitter Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta property="twitter:domain" content="cornucopia.owasp.org">
    <meta property="twitter:url" content="https://cornucopia.owasp.org/">
    <meta name="twitter:title" content="{$t('layout.title')}">
    <meta name="twitter:description" content="{$t('layout.twitter.description')}">
    <meta name="twitter:image" content="/images/opengraph.png">
    <!-- END of Tags -->
</svelte:head>
