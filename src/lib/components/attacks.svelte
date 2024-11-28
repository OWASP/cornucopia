<script lang="ts">
    import { type Attack } from "$lib/cardAttacks";
    import MobileAppCardMapping from "./mobileAppCardMapping.svelte";
    export let mappings;
    export let attacks;
      
  </script>
    {#each attacks as attack}
      <p><a href="/taxonomy/attacks/{attack.url}">{attack.name}</a></p>
    {:else}
      <p>No attacks registered!</p>
    {/each}
  
  <style>
    p {
      font-size: 1.5rem;
    }
    h1,
    a,
    p {
      color: var(--background);
      font-family: var(--font-title);
      font-weight: 400;
    }
  
    .title {
      background: var(--background);
      color: white;
      padding: 0.5rem;
    }
  </style>
  