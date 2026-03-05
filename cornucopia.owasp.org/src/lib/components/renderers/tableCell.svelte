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
    td
    {
      padding: 0.25rem;
      text-align: left;
    }
    th
    {
      padding: 0.25rem;
      font-weight: bold;
      background: linear-gradient(0deg, rgba(0, 0, 0, 0.1) 90%, rgba(255,255,255,0.3) 100%);
    }
  </style>