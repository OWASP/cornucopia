<script lang="ts">
    interface Props {
        href: string;
    }

    let { href }: Props = $props();
</script>
<div id="chevron">
    <a href="{href}"><img alt="go-down" src="icons/chevron.png"/></a>
</div>
<style>   

    a
    {
        display: block;
    }

    #chevron
    {
        transform: rotate(180deg);
        position: sticky;
        display: block;
        height : 6vw;
        margin-right: 42vw;
        top: calc(80% - 20vh);
        /*bottom:-3rem;*/
        cursor:pointer;
        transition: var(--transition);
        filter:invert();
        z-index: 99;
    }

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
            top: calc(70% - -20vh);
            position: absolute;
            left: calc(50% - 5vw);
        }
    }
</style>