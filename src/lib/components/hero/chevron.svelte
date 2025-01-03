<script lang="ts">
    export let href: string;
    export let style : string = "";
</script>
<div id="chevron">
    <a href="{href}"><img {style} alt="go-down" src="icons/chevron.png"/></a>
</div>
<style>   

    a
    {
        display: block;
    }

    #chevron
    {
        transform: translate(0,0rem) rotate(180deg);
        position: absolute;
        display: block;
        width : 20vw;
        height : 6vw;
        left: calc(50% - 16vw);
        top: calc(80% - 20vh);
        bottom:-3rem;
        cursor:pointer;
        transition: var(--transition);
        filter:invert();
        padding: 1rem;
        z-index: 100;
;    }

     img {
        width : 10vw;
     }

    #chevron:hover
    {
        opacity: 50%;
        transform: translate(0,1rem) rotate(180deg);
    }

    @media (max-aspect-ratio: 1/1) 
    {
        #chevron
        {
            top: calc(80% - 15vh);
        }
    }
</style>