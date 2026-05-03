<!--
@component
Renders a markdown table body section as a `<tbody>` element.
-->
<script lang="ts">
    import type { Snippet } from 'svelte'

    interface Props {
        children?: Snippet
    }
    const { children }: Props = $props()
</script>

<tbody>{@render children?.()}</tbody>
