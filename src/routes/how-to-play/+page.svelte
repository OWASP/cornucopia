<script>
  import SvelteMarkdown from 'svelte-markdown';
  import renderers from '$lib/components/renderers/renderers';
  import {readLang} from "$lib/stores/stores";
  export let data;
  const lang = readLang();
  let content = data.content.get($lang) || data.content.get('en');
</script>
{#if content != ''}
<SvelteMarkdown {renderers} source={content}></SvelteMarkdown>
{/if}

  <style>
    h2
    {
        font-weight: bold;
    }
    p,li
    {
      color:var(--background);
    }
    a,p,li
    {
        font-size: 1.3rem;
        font-family: var(--font-body);
        text-align: justify;
    }
    div
    {
        font-size: 1.2rem;
    }

    iframe
    {
        width : 100%;
        height : 100%;
        min-height: 28.58rem;
    }

    a
    {
        display: inline-block;
        text-decoration: none;
        font-weight: bold;
        color:var(--background);
    }

    a:hover
    {
        opacity: 70%;
        color: rgb(41, 0, 176);
    }

    @media (max-aspect-ratio: 1/1) 
    {
       div
       {
        margin:auto;
        width : 90%;
       } 
    }
  </style>
