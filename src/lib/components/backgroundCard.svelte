<script lang="ts">
    interface Props {
        url: string;
        position: number;
    }

    let { url, position }: Props = $props();

    function getStyle() : string
    {
        // Make sure cards are rendered in correct order
        let zIndex : string = "z-index:" + Math.abs(position)*(-50) + ";";

        // Darken card that are more towards the back
        let filter : string = "filter:brightness(" + (70-Math.abs(position*25)) + "%);";

        // Transform cards left and right depending on order
        let transform = "transform:translate(" + (6*position + 2) + "vw,0);";

        // Set the correct card image url as background 
        let backgroundImage : string = "background-image:linear-gradient(to bottom, rgba(255, 255, 255, 0.3), rgba(0, 0, 0, 0.2)),url('" + url + "');";

        // Concatenate all properties together in a string
        return zIndex + filter + transform + backgroundImage;
    }
</script>

<div class="card-preview">
    <div class="card" style="{getStyle()}"></div>
</div>

<style>
    .card
    {
        width : 20vw;
        position: absolute;
        top : 15rem;
        aspect-ratio: 20/32;
        border-radius: 1.2rem;
        background-position: 50% 50%;
        background-size: 117%;
        transition: var(--transition);
    }

    @media (max-aspect-ratio: 1/1)
    {
        .card
        {
            display: none;
            width : 20vh;
        }
    }
</style>