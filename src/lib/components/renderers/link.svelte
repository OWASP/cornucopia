<script lang="ts">
    export let href = '';
    export let title : string = "";
    export let raw : string = "";

    let target : string = "_blank";
    let rel : string = '';
    let clazz : string = "";
    let style : string = "";

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
      style = 'color:white;';
    }
  </script>
  
  <a {rel} {target} {href} {title} class={clazz} {style}><slot></slot></a>

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
  </style>