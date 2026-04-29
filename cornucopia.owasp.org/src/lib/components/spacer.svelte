<script lang="ts">
interface Props {
height?: string;
}
let { height = '5rem' }: Props = $props();
</script>
<div class="spacer" style="height: {height}"></div>
<style>
.spacer {
width: 100%;
}
</style>