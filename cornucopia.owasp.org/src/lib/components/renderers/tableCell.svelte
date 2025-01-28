<script lang="ts">
  interface Props {
    header: any;
    align: any;
    children?: import('svelte').Snippet;
  }

  let { header, align, children }: Props = $props();
  </script>
  
  {#if header}
    <th {align}>{@render children?.()}</th>
  {:else}
    <td {align}>{@render children?.()}</td>
  {/if}

  <style>
    td,th
    {
      padding: 0.25rem;
      text-align: left;
    }
  </style>