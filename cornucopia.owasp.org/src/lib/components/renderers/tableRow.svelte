<!--
@component
Renders a markdown table row as a `<tr>` element.
-->
<script lang="ts">
    import type { Snippet } from 'svelte'

    interface Props {
        children?: Snippet
    }
    const { children }: Props = $props()
</script>

<tr>{@render children?.()}</tr>
