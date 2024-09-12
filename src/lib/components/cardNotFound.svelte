<script lang="ts">
    import {type Card} from "../../domain/card/card"
    export let card : Card;
</script>

<p>Unknown card: {String(card.card).toUpperCase()} {card.suit}</p>

<style>
    p {
        color: red;
    }
</style>
