<script lang="ts">
    export let href: string;
    export let style : string = "";
</script>

<a href="{href}"><img {style} alt="go-down" src="icons/chevron.png"/></a>

<style>   

    a
    {
        display: block;
    }
    img
    {
        transform: translate(0,0rem) rotate(180deg);
        position: absolute;
        display: block;
        width : 6vw;
        height : 6vw;
        left: calc(50% - 2rem);
        top: calc(80% - 1vh);
        bottom:-3rem;
        cursor:pointer;
        transition: var(--transition);
        filter:invert();
        padding: 1rem;
;    }

    img:hover
    {
        opacity: 50%;
        transform: translate(0,1rem) rotate(180deg);
    }

    @media (max-aspect-ratio: 1/1) 
    {
        img
        {
            bottom:0rem;
            top: calc(50% - 10vh);
        }
    }
</style>