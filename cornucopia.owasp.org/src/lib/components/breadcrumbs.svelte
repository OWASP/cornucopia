<script lang="ts">
    import { run } from 'svelte/legacy';

    import { page } from "$app/stores";
    import { Text } from "$lib/utils/text";

    let parts : string[] = $state();

    run(() => {
        parts = $page.url.pathname.split('/');
    });

    function generateHref(index : number, input : string) : string
    {
        let result = "";
        for(let i = 0 ; i < index + 1 ; i++)
        {
            result += parts[i] + '/';
        }
        return result;
    }

    function generateName(index : number, input : string)
    {
        if(input == '')
            return 'Home'
        else
            return Text.FormatPlain(input);
    }
    
</script>

{#if $page.url.pathname != '/' && $page.status < 400 }
    <p id="breadcrumbs">
        {#each parts as part,index}
            {#if index != 0}
                <span>{'>'} </span>
            {/if}

            {#if parts[index-1] && parts[index-1] == 'cards'}
                <a title="OWASP Cornucopia: {generateName(index,part)}" class="card-code" href="{generateHref(index,part)}">{generateName(index,part)}</a>
            {:else}
                <a title="OWASP Cornucopia: {generateName(index,part)}" href="{generateHref(index,part)}">{generateName(index,part)}</a>
            {/if}
            <span> </span>
        {/each}
    </p>
{/if}

<style>
    p
    {
        padding-top: 5.5rem;
        font-size: 1.5rem;
        font-weight: bold;
        text-decoration: none;
        margin:0;
    }

    a:hover
    {
        opacity: 50%;
    }

    a
    {
        text-decoration: none;
        color:var(--background);
        transition: var(--transition);
    }

    .card-code 
    {
        text-transform: uppercase;
    }
    @media (max-aspect-ratio: 1/1)
    {
        #breadcrumbs
        {
            margin: 0rem 1rem;
        }
    }
</style>