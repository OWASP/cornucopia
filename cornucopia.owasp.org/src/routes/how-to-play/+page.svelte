<script>
  import SvelteMarkdown from 'svelte-markdown';
  import { renderers }  from '$lib/components/renderers/renderers';
  import {readLang, readTranslation} from "$lib/stores/stores";
  /** @type {{data: any}} */
  let { data } = $props();
  let t = readTranslation();
  const lang = readLang();
  let content = data.content.get($lang) || data.content.get('en');
</script>
<svelte:head>
    <title>{$t('printing.head.title')}</title>
    <link rel="canonical" href="https://cornucopia.owasp.org/how-to-play" />
    <meta name="description" content="{$t('play.head.description')}" />
	<meta name="keywords" content="{$t('play.head.keywords')}" />
    <meta property="og:title" content="{$t('play.head.title')}">
    <meta property="og:description" content="{$t('play.head.description')}">
    <meta name="twitter:title" content="{$t('play.head.title')}">
    <meta name="twitter:description" content="{$t('play.head.description')}">
</svelte:head>
<div>
{#if content != ''}
<SvelteMarkdown {renderers} source={content}></SvelteMarkdown>
{/if}
</div>
  <style>


    @media (max-aspect-ratio: 1/1) 
    {
       div
       {
        margin: 0rem 1rem;
       }
    }
  </style>
