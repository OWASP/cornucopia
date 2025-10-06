<script>
    import Author from "$lib/components/author.svelte";

    import {readTranslation} from "$lib/stores/stores";
    let t = readTranslation();
    /** @type {{data: any}} */
    let { data } = $props();
</script>
<svelte:head>
    <title>{$t('author.head.title')}</title>
    <link rel="canonical" href="https://cornucopia.owasp.org/author" />
    <meta name="description" content="{$t('author.head.description')}" />
	<meta name="keywords" content="{$t('author.head.keywords')}" />
    <meta property="og:title" content="{$t('author.head.title')}">
    <meta property="og:description" content="{$t('author.head.description')}">
    <meta name="twitter:title" content="{$t('author.head.title')}">
    <meta name="twitter:description" content="{$t('author.head.description')}">
</svelte:head>
<div>
<h1>{$t('news.author.h1')}</h1>

<div class="container">
    {#each data.authors as author}
        <Author {author}></Author>
    {/each}
</div>
</div>
<style>
    .container
    {
        width : 100%;
        display: flex;
        justify-content: space-between;
        flex-direction: row;
        flex-wrap: wrap;
    }

    
    @media (max-aspect-ratio: 1/1) 
    {
        div
        {
            margin: 0rem 1rem;
        }
        .container
        {
            justify-content: center;
            flex-direction: column;
            margin: auto;
        } 
    }
</style>
