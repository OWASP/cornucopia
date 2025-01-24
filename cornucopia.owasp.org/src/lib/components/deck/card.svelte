<script lang="ts">
    import { fly } from "svelte/transition";
    interface Props {
        index: number;
        reset: any;
        image: string;
    }

    let { index, reset, image }: Props = $props();

    let hover : boolean = $state(false);

    function mouseenter()
    {
        hover = true;
    }

    function mouseleave()
    {
        hover = false;
    }
</script>

<div 
role='button'
tabindex="-1"
onkeydown={reset} 
onclick={reset}
onmouseenter={mouseenter}
onmouseleave={mouseleave}
in:fly="{{ y: 100, duration: 1000 , delay: index * 100}}" 
class="card card-{index}"></div>


<style>
    .card
    {
        left: 70%;
        top : 30%;
        position: absolute;
        width : 17vw;
        aspect-ratio: 20/32;
        border-radius: 1.2rem;
        background-position: 50% 50%;
        background-size: 117%;
        transition: var(--transition);
        transform-origin: 0 100%;
        box-shadow: rgba(50, 50, 93, 0.25) 0px 13px 27px -5px, rgba(0, 0, 0, 0.3) 0px 8px 16px -8px;
        filter:saturate(1.5);
        cursor:pointer;
    }

    .card-0
    {
        transform: translate(0,0) rotate(-35deg);
        background-image:linear-gradient(to bottom, rgba(255, 255, 255, 0.3), rgba(0, 0, 0, 0.2));
    }
    .card-1
    {
        transform: translate(0,0) rotate(-25deg);
        background-image:linear-gradient(to bottom, rgba(255, 255, 255, 0.3), rgba(0, 0, 0, 0.2));
    }
    .card-2
    {
        transform: translate(0,0) rotate(-15deg);
        background-image:linear-gradient(to bottom, rgba(255, 255, 255, 0.3), rgba(0, 0, 0, 0.2));
    }
    .card-3
    {
        transform: translate(0,0) rotate(-5deg);
        background-image:linear-gradient(to bottom, rgba(255, 255, 255, 0.3), rgba(0, 0, 0, 0.2));
    }
    .card-4
    {
        transform: translate(0,0) rotate(5deg);
        background-image:linear-gradient(to bottom, rgba(255, 255, 255, 0.3), rgba(0, 0, 0, 0.2));
    }
    .card-5
    {
        transform: translate(0,0) rotate(15deg);
        background-image:linear-gradient(to bottom, rgba(255, 255, 255, 0.3), rgba(0, 0, 0, 0.2));
    }
    .card-6
    {
        transform: translate(0,0) rotate(25deg);
        background-image:linear-gradient(to bottom, rgba(255, 255, 255, 0.3), rgba(0, 0, 0, 0.2));
    }

    .card:hover
    {
        filter:brightness(1.1);
    }

    @media (max-aspect-ratio: 1/1) 
    {
        .card
        {
            left: 45%;
            top : 65%;
            width : 35vw;
        }
    }
</style>