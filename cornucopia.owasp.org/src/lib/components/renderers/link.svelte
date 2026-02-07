<script lang="ts">
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

    let target = $derived(href.startsWith('/') || href.startsWith('#') ? '_self' : '_blank');
    let rel = $derived.by(() => {
      if (raw.includes('[internal]')) return 'noopener';
      if (raw.includes('[external]')) return 'noopener nofollow';
      return '';
    });
    let clazz = $derived(raw.includes('[inline]') ? 'inline' : '');
    let style = $derived(raw.includes('[white]') ? ' white' : '');
  </script>
  
  <a {rel} {target} {href} {title} class="{clazz} link-with-external-indicator{style}">{@render children?.()}</a>

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