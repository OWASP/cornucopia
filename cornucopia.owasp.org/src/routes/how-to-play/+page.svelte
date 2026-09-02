<script>
    import Metadata from "$lib/components/metadata.svelte";
  import SvelteMarkdown from 'svelte-markdown';
  import { renderers }  from '$lib/components/renderers/renderers';
  import {readLang} from "$lib/stores/stores";
  /** @type {{data: any}} */
  let { data } = $props();
  const lang = readLang();
  let content = $derived(data.content.get($lang) || data.content.get('en'));
</script>
{#if data.metadata}<Metadata metadata={data.metadata} />{/if}
<div>
{#if content != ''}
<SvelteMarkdown {renderers} source={content}></SvelteMarkdown>
{/if}
</div>
  <style>


    @media (max-width: 767px) 
    {
       div
       {
        margin: 0rem 1rem;
       }
    }
  </style>
