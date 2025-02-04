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

    let target : string = $state("_blank");
    let rel : string = $state('');
    let clazz : string = $state("");
    let style : string = $state("");

    if(href.startsWith('/'))
      target = '_self';

    if (raw.includes('[internal]')) {
      rel = 'noopener';
    }

    if (raw.includes('[external]')) {
      rel = 'noopener nofollow';
    }

    if (raw.includes('[inline]')) {
      clazz = 'inline';
    }

    if (raw.includes('[white]')) {
      style = ' white';
    }
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