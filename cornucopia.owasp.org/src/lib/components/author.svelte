<script lang="ts">
    import { goto } from "$app/navigation";
    import { Text } from "$lib/utils/text";
    import type { Author } from "../../domain/author/author";
    interface Props {
        author: Author;
    }

    let { author }: Props = $props();
</script>

<button
onclick={()=>goto("/author/" + author.name)}>
    <img alt={author.name} src="./data/author/{author.name}/profile-picture.jpg"/>
    <p>{Text.Format(author.name)}</p>
</button>


<style>
    p
    {
        font-family: var(--font-title);
        font-size: 1.2rem;
        margin:0;
        padding: .2rem
    }

    img
    {
        width : 100%;
        filter:saturate(0);
        transition: var(--transition);
    }

    img:hover
    {
        filter:saturate(1)
    }

    button
    {
        padding:0;
        width : 20%;
        background: none;
        border:none;
        background-color: var(--white);
        color: var(--background);
        margin: 1rem;
        outline: 3px white solid;
        cursor:pointer;
    }

    @media (max-aspect-ratio: 1/1) 
    {
        button
        {
            width : 50%;
            margin:auto;
            margin-bottom: 3rem;
        }
    }
</style>