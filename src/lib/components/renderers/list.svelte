<script lang="ts">
  interface Props {
    ordered: any;
    start: any;
    children?: import('svelte').Snippet;
  }

  let { ordered, start, children }: Props = $props();
</script>
  
  {#if ordered}
    <ol {start}>{@render children?.()}</ol>
  {:else}
    <ul>{@render children?.()}</ul>
  {/if}

<style>
  ul,ol
  {
    list-style-position: outside;
    overflow: hidden;
    margin-top: 1rem;
    font-size: 1.2rem;
    margin-top: 0;
    opacity: 90%;
  }
  ul
  {
    list-style-type: none;
  }
</style>