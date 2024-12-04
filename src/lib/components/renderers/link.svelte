<script lang="ts">
    export let href = ''
    export let title : string = ""

    let target : string = "_blank";
    let rel : string = 'noopener';

    if(href.startsWith('/'))
      target = '_self';
      rel = '';
  </script>
  
  <a {rel} {target} {href} {title}><slot></slot></a>

  <style>
    a
    {
        padding : .10rem;
        border-radius: .25rem;
        color:var(--background);
        font-weight: bold;
        transition: var(--transition);
    }

    a:hover
    {
        opacity: 50%;
    }    
  </style>