<script lang="ts">
    import { fly } from "svelte/transition";
    export let index : number;
    export let reset : any;
    export let image : string;

    let hover : boolean = false;
    
    // TODO: clean up this mess
    function generateStyle(hover : boolean) : string
    {
        let rotation : number = (index*10-45);

        return "transform:translate("  
        + "0,0" 
        + ")"
        + " rotate(" 
        + rotation
        + "deg);background-image:linear-gradient(to bottom, rgba(255, 255, 255, 0.3), rgba(0, 0, 0, 0.2)),url(" 
        + image 
        + ")";
    }

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
data-umami-event="card-deck-frontpage-button"
tabindex="-1"
on:keydown={reset} 
on:click={reset}
on:mouseenter={mouseenter}
on:mouseleave={mouseleave}
in:fly="{{ y: 100, duration: 1000 , delay: index * 100}}" 
class="card" 
style={generateStyle(hover)}/>


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