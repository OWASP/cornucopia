<script lang="ts">
    export let header : any
    export let align : any
  </script>
  
  {#if header}
    <th {align}><slot></slot></th>
  {:else}
    <td {align}><slot></slot></td>
  {/if}

  <style>
    td,th
    {
      padding: 0.25rem;
      text-align: left;
    }
  </style>