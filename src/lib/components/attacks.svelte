<script lang="ts">
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
    a,
    p {
      color: var(--background);
      font-family: var(--font-title);
      font-weight: 400;
    }
  </style>
  