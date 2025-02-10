<script lang="ts">
    import { error } from '@sveltejs/kit';
    import {type Card} from "../../domain/card/card"
    interface Props {
        card: string;
    }

    let { card }: Props = $props();
    error(404, {
			message: `Unknown card: ${String(card).toUpperCase()}`
    });
</script>

<p>Unknown card: {String(card).toUpperCase()}</p>

<style>
    p {
        color: red;
    }
</style>
