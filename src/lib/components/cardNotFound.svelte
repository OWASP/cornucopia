<script lang="ts">
    import {type Card} from "../../domain/card/card"
    interface Props {
        card: Card;
    }

    let { card }: Props = $props();
</script>

<p>Unknown card: {String(card.id).toUpperCase()} {card.suit}</p>

<style>
    p {
        color: red;
    }
</style>
