<script lang="ts">
  import { resolve } from "$app/paths";
  import { getMappingUrl } from "../../domain/mapping/mappingController";
  import { isLocalMappingLink, resolveMappingLink } from "./mappingsListLinks";

  interface Props {
    title: string;
    mappings: number[] | string[];
    linkFunction?: (m: string | number) => string;
    textFunction?: (m: string | number) => string;
    mappingAttribute?: string;
    urlTemplates?: Record<string, string>;
  }

  let {
    title,
    mappings,
    linkFunction = undefined,
    textFunction = undefined,
    mappingAttribute = undefined,
    urlTemplates = {},
  }: Props = $props();

  function getLink(mapping: string | number): string | undefined {
    const link = linkFunction?.(mapping) ?? getMappingUrl(urlTemplates, mappingAttribute, mapping);
    return link || undefined;
  }

  function isLocalLink(mapping: string | number): boolean {
    return isLocalMappingLink(getLink(mapping));
  }

  function resolveDataDrivenPath(path: string): string {
    // Mapping URLs are data-driven, so their route cannot be inferred from generated route types.
    return resolve(...([path] as never));
  }

  function getResolvedLink(mapping: string | number): string | undefined {
    return resolveMappingLink(getLink(mapping), resolveDataDrivenPath);
  }
</script>

<p>
  <span class="title">{title}</span>
  {#each mappings as m, index (index)}
    {#if getLink(m) == undefined}
      <span>{m}</span>{#if index != mappings.length - 1}<span class="spacer">, </span>{/if}
    {:else if String(m).trim() != '-' && isLocalLink(m) && textFunction != undefined }
      <a
        title="{title} {textFunction(m)}"
        href={getResolvedLink(m)}
      >
        {textFunction(m)}
      </a>{#if index != mappings.length - 1}<span class="spacer">, </span>{/if}
    {:else if String(m).trim() != '-' && isLocalLink(m)}
      <a
        title="{title} {m}"
        href={getResolvedLink(m)}
      >
        {m}
      </a>{#if index != mappings.length - 1}<span class="spacer">, </span>{/if}
    {:else if String(m).trim() != '-'}
      <a
        title="{title} {m}"
        target="_blank"
        rel="noopener nofollow external"
        class="link-with-external-indicator"
        href={getResolvedLink(m)}
      >{m}</a>{#if index != mappings.length - 1}<span class="spacer">, </span>{/if}
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
