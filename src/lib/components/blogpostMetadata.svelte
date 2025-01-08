<script lang="ts">
    import { goto } from "$app/navigation";
    import { Text } from "$lib/utils/text";
    import type { Blogpost } from "../../domain/blogpost/blogpost";

    interface Props {
        blogpost: Blogpost;
    }

    let { blogpost }: Props = $props();

    let authorLink : string = '/author/' + blogpost.author;
</script>

<div class="metadata">
    <div class="left">
        <p>Date: {Text.FormatDate(blogpost.date)}</p>
        <p>Author: <a href="{authorLink}">{Text.Format(blogpost.author)}</a></p>
        <p>Tags: 
            {#each blogpost.tags || [] as tag}
            <a class="tag" href="/news">{Text.Format(tag)}</a><span></span>
            {/each}
        </p>
    </div>
    <div class="right">
        <button onclick={()=>goto(authorLink)}>
        <img title="{Text.Format(blogpost.author)}" alt="{blogpost.author} profile picture" src="/data/author/{blogpost.author}/profile-picture.jpg"/>
        </button>
    </div>
</div>

<style>
    .tag
    {
        padding: .25rem;
        color:var(--background);
        background-color: var(--white);
        margin: .25rem;
        text-decoration: none;
    }

    .tag:hover
    {
        opacity: 70%;
    }
    .metadata
    {
        display: flex;
        padding-bottom: 2rem;
    }


    img
    {
        width : 5rem;
        outline: 1px white solid;
        cursor:pointer;
        margin: 1rem;   
    }

    img:hover
    {
        opacity: 70%;
    }

    button
    {
        background: none;
        border:none;
    }
</style>
