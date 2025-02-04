<script lang="ts">
    import { readTranslation } from "$lib/stores/stores";
  interface Props {
    attacks: any;
  }

  let { attacks }: Props = $props();
    let t = readTranslation();
  </script>
    {#each attacks as attack}
      <p><a href="/taxonomy/attacks/{attack.url}">{attack.name}</a></p>
    {:else}
      <p>{$t('cards.attacks.p1')}</p>
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
  