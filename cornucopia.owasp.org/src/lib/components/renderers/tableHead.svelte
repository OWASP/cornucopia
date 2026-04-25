<!--
@component
Renders a markdown table header section as a `<thead>` element.
-->
<script lang="ts">
    import type { Snippet } from 'svelte'

    interface Props {
        children?: Snippet
    }
    const { children }: Props = $props()
</script>

<thead>{@render children?.()}</thead>


  <style>
    thead
    {
      padding: 0.25rem;
      
    }
  </style>