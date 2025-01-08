<script lang="ts">
    import { fly } from "svelte/transition";
    interface Props {
        index: number;
        reset: any;
        image: string;
    }

    let { index, reset, image }: Props = $props();

    let hover : boolean = $state(false);
    
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
tabindex="-1"
onkeydown={reset} 
onclick={reset}
onmouseenter={mouseenter}
onmouseleave={mouseleave}
in:fly="{{ y: 100, duration: 1000 , delay: index * 100}}" 
class="card" 
style={generateStyle(hover)}></div>


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