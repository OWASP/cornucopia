<script lang="ts">
  import { resolve } from "$app/paths";

  interface Props {
    href?: string;
    title?: string;
    raw?: string;
    children?: import('svelte').Snippet;
  }

  let {
    href = '',
    title = "",
    raw = "",
    children
  }: Props = $props();
  $effect(() => {
    console.log('raw:', raw);
  });
  let target = $derived((href.startsWith('/') || href.startsWith('#') || raw.includes('[blank]')) ? '_self' : '_blank');
  let clazz = $derived(raw.includes('[inline]') ? 'inline' : '');
  let style = $derived(raw.includes('[white]') ? ' white' : '');
</script>
  
  {#if href.startsWith('/') || href.startsWith('#')}
    <a target={target} rel="noopener" href={resolve(href)} {title} class="{clazz} link-with-external-indicator{style}">{@render children?.()}</a>
  {:else if raw.includes('[external]')}
    <a target={target} rel="noopener nofollow external" href={href} {title} class="{clazz} link-with-external-indicator{style}">{@render children?.()}</a>
  {:else}
    <a target={target} rel="external" href={href} {title} class="{clazz} link-with-external-indicator{style}">{@render children?.()}</a>
  {/if}

  <style>
    a
    {
        padding : .10rem;
        border-radius: .25rem;
        color:var(--background);
        text-decoration: underline;
        transition: var(--transition);
    }

    a:hover
    {
        opacity: 50%;
        text-decoration: none;
    }
    
    .white {
      color:white;
    }
  </style>