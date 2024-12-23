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