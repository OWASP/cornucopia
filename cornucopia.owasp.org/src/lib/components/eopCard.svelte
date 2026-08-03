<script lang="ts">
    import type { Card } from "../../domain/card/card";
    import type { CardImage } from "$lib/services/cardImagesService";
    import type { SuitStyling } from "$lib/services/suitStylingService";
    import "./eopCard.css";

    interface Props {
        card?: Card;
        cardImages?: Record<string, CardImage>;
        suitStyling?: Record<string, SuitStyling>;
    }

    let { card, cardImages = undefined, suitStyling = undefined }: Props = $props();

    let cardImage = $derived(cardImages?.[card?.id ?? '']);
    let suitStyle = $derived(suitStyling?.[card?.suit ?? '']);

    // handles the conversion of the value for the EoP cards between the copi and cornucopia codebases
    function eopValue(value: string)
    {
        return value === 'X' ? '10' : value;
    }
</script>

<div
    class="card-render eop {card?.suit} n{eopValue(card?.value)}"
    class:opaque={!!cardImage?.opaque}
    style={suitStyle ? `--eop-tab:${suitStyle.tab}; --eop-watermark:${suitStyle.watermark}; --eop-royal:${suitStyle.royal};` : ''}
>
    {#if !['J', 'Q', 'K'].includes(card?.value)}
        <span class="watermark" aria-hidden="true">{eopValue(card?.value)}</span>
    {/if}
    <div class="artwork" style={cardImage ? `background-image:url(${cardImage.image});` : ''}></div>
    <div class="number-tab"><span>{eopValue(card?.value)}</span></div>
    <div class="text-block">
        <p class="suit-name">{card?.suitName}</p>
        <p class="description">{card?.desc}</p>
    </div>
</div>
