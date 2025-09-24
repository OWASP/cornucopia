<script lang="ts">
  interface Props {
    title: string;
    mappings: number[] | string[];
    linkFunction?: any;
    textFunction?: any;
  }

  let { title, mappings, linkFunction = undefined, textFunction = undefined }: Props = $props();
</script>

<p>
  <span class="title">{title}</span>
  {#each mappings as m, index}
    {#if linkFunction == undefined}
      <span>{m}</span>{#if index != mappings.length - 1}<span class="spacer">, </span>{/if}
    {:else if String(m).trim() != '-' && linkFunction(m).startsWith('/') && textFunction != undefined }
      <a title="{title} {textFunction(m)}" href={linkFunction(m)}>{textFunction(m)}</a>{#if index != mappings.length - 1}<span class="spacer">, </span>{/if}
    {:else if String(m).trim() != '-' && linkFunction(m).startsWith('/')}
      <a title="{title} {m}" href={linkFunction(m)}>{m}</a>{#if index != mappings.length - 1}<span class="spacer">, </span>{/if}
    {:else if String(m).trim() != '-'}
      <a title="{title} {m}" target="_blank" rel="noopener nofollow" class="link-with-external-indicator" href={linkFunction(m)}>{m}</a>{#if index != mappings.length - 1}<span class="spacer">, </span>{/if}
    {:else}
      <span>{m}</span>{#if index != mappings.length - 1}<span class="spacer">, </span>{/if}
    {/if}
  {/each}
</p>

<style>
  p,
  a {
    color: var(--background);
    font-family: var(--font-title);
    font-weight: 400;
    font-size: 1.5rem;
  }

  p {
    width: 100%;
    word-break: break-all;
    white-space: normal;
  }

  .spacer {
    padding-right: 0.2rem;
  }

  .title {
    font-weight: 600;
  }
</style>
