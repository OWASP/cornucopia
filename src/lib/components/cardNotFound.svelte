<script lang="ts">
    import {type Card} from "../../domain/card/card"
    export let card : Card;
</script>

<p>Unknown card: {card.card} {card.suit}</p>

<style>
    p {
        color: red;
    }
</style>
