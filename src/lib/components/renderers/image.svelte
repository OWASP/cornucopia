<script lang="ts">
    import { page } from "$app/stores";

  interface Props {
    href?: string;
    title?: string;
    text?: string;
  }

  let { href = $bindable(''), title = $bindable(""), text = $bindable('') }: Props = $props();

    let url : string = '/data' + $page.url.pathname + '/' + href

    // Using /static allows autocomplete in VS code somehow, but breaks the image linking
    // So I just remove it before applying the href property of the img tag.
    if(href.includes("/static"))
        href = href.replace("/static","");


    let small : boolean = false;
    if(text.includes("[small]"))
    {
        small = true;
        text = text.replace("[small]","")
    }

    let medium : boolean = false;
    if(text.includes("[medium]"))
    {
        medium = true;
        text = text.replace("[medium]","")
    }

    if(!title || title == "")
        title = text;

    function getStyle()
    {
        if(small)
            return "small";

        if(medium)
            return "medium";

        return "";
    }

  </script>
  
  <img loading="lazy" class="{getStyle()}" src={url} {title} alt={text}>
  <p class="alt-text"><i>Image: {text}</i></p>

  <style>
        .alt-text
        {
            font-weight: 300;
            font-size: 1rem;
            text-align: center;
            margin-bottom: 2rem;
        }

        img
        {
            width : 100%;
            border-radius: .5rem;
            margin:auto;
            margin-top: 2rem;
            margin-bottom: 1rem;;
            display: block;
        }

        img.small 
        {
            width:25%;
        }

        img.medium
        {
            width:50%;
        }

        @media (max-aspect-ratio: 1/1) 
        {
            img
            {
                width : 100% !important;
            }
        }
  </style>