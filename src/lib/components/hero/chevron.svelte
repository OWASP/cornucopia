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
        width : 100%;
        height : 100%;
        transform: translate(0,0rem) rotate(180deg);
        position: absolute;
        display: block;
        width : 4rem;
        height : 4rem;
        left: calc(50% - 2rem);
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
        }
    }
</style>