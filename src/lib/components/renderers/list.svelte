<script lang="ts">
    export let ordered : any
    export let start : any
</script>
  
  {#if ordered}
    <ol {start}><slot></slot></ol>
  {:else}
    <ul><slot></slot></ul>
  {/if}

<style>
  ul,ol
  {
    list-style-position: inside;
    overflow: hidden;
    margin-top: 1rem;
    font-size: 1.2rem;
    margin-top: 0;
    opacity: 90%;
  }
</style>