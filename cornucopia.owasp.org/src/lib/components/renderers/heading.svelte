<script lang="ts">
    import { goto } from "$app/navigation";

  interface Props {
    depth: number;
    raw: string;
    text: string;
    children?: import('svelte').Snippet;
  }

  let {
    depth,
    raw,
    text,
    children
  }: Props = $props();

    function cleanText(input : string) : string
    {
      return input.trim().replaceAll(':','').replaceAll(' ','-').replaceAll(',','').replaceAll("'","")
    }
</script>
  
  {#if depth === 1}
    <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
    <h1 title="{text}" class="clickable" onkeydown={()=>goto("#" + cleanText(text))} onclick={()=>goto("#" + cleanText(text))}
     id={cleanText(text)}>
      {@render children?.()}
    </h1>
  {:else if depth === 2}
      <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
    <h2 title="{text}" class="clickable" onkeydown={()=>goto("#" + cleanText(text))} onclick={()=>goto("#" + cleanText(text))} id={cleanText(text)}>
      {@render children?.()}
    </h2>
  {:else if depth === 3}
    <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
    <h3 title="{text}" class="clickable" onkeydown={()=>goto("#" + cleanText(text))} onclick={()=>goto("#" + cleanText(text))} id={cleanText(text)}>
      {@render children?.()}
    </h3>
  {:else if depth === 4}
    <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
    <h4 title="{text}" class="clickable" onkeydown={()=>goto("#" + cleanText(text))} onclick={()=>goto("#" + cleanText(text))} id={cleanText(text)}>
      {@render children?.()}
    </h4>
  {:else if depth === 5}
    <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->

    <h5 title="{text}" class="clickable" onkeydown={()=>goto("#" + cleanText(text))} onclick={()=>goto("#" + cleanText(text))} id={cleanText(text)}>
      {@render children?.()}
    </h5>
  {:else if depth === 6}
    <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
    <h6 title="{text}" class="clickable" onkeydown={()=>goto("#" + cleanText(text))} onclick={()=>goto("#" + cleanText(text))} id={cleanText(text)}>
      {@render children?.()}
    </h6>
  {:else}
    {raw}
  {/if}

  <style>
    .clickable
    {
      cursor:pointer;
    }

    .clickable:hover
    {
      opacity: 70%;
    }
    h1
    {
      font-size: 2.2rem;
      padding: .5rem;
      font-weight: bolder;
    }
    h2
    {
      font-size: 1.8rem;
      padding: .5rem .5rem .5rem 0;
      font-weight: bold;
     }

    h3
    {
      font-size: 1.6rem;
      padding-top: .5rem;
      padding-bottom: .5rem;
      font-size: 1.2rem;
      font-weight: bolder;
      opacity: 90%;
    }
    h4
    {
      padding-top: .3rem;
      padding-bottom: .3rem;
      font-size: 1.4rem;
      font-weight: bold;
      opacity: 90%;
    }
    h5
    {
      padding-top: .2rem;
      padding-bottom: .2rem;
      font-size: 1.2rem;
      font-weight: bolder;
      opacity: 90%;
    }
    h6
    {
      padding-top: .2rem;
      padding-bottom: .2rem;
      font-size: 1rem;
      font-weight: bold;
      opacity: 90%;
    }
 
  </style>