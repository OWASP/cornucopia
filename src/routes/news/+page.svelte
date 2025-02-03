<script>
    import { goto } from '$app/navigation';
    import { Text } from '$lib/utils/text';

    export let data;
</script>

<h1>News</h1>
<p>Wondering what's new with Cornucopia? This is the place to look!</p>

{#if data.posts.length == 0}
<p>No blogposts have been published yet, come back soon!</p>
{:else}
    <div class="list">
        {#each data.posts as post}
            <button data-umami-event="blogpost-button" title="View {Text.Format(post.path)}" on:click={()=>goto('/news/' + post.path)}>
                <p class="title">{Text.Format(post.title)}</p>
                <p class="info">
                    {Text.FormatDate(post.date)}
                     • 
                    {Text.Format(post.author)}
                    <a class= "link" href="/news/{post.path}">>> Read more</a>
                </p>
            </button>
        {/each}
    </div>
{/if}


<p>View <a href="/author">All authors</a></p>
{#each data.authors as author}
    <p style="display:none;">
        <a href="/author/{author.name}">{author.name}</a>
    </p>
{/each}


<style>
    a
    {
        font-weight: bold;
        text-decoration: none;
        transition: var(--transition);
        color: var(--background)
    }

    a:hover
    {
        opacity: 50%;
    }

    .link
    {
        display: none;
    }
    .info
    {
        font-size: 1rem;
        margin: 1rem;
    }

    .title
    {
        background-color: rgba(255, 255, 255, 0.237);
        margin: 0;
        padding: .5rem;
        border-top-left-radius: .5rem;
        border-top-right-radius: .5rem;
    }
    button
    {
        padding: 1rem;
        width : calc(50% - 4rem);
        margin: 1rem;
        text-align: left;
        font-weight: 400;
        background: none;
        border:none;
        cursor:pointer;
        color:var(--background);
        outline: 1px white solid;
        margin-bottom: 4rem;
        background: white;
        border-radius: .5rem;
        transition: var(--transition);
		outline: 1px rgb(231, 231, 231) solid;

        box-shadow: rgba(255, 255, 255, 0.1) 0px 1px 1px 0px inset, rgba(50, 50, 93, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px;
    }

    button:hover
    {
        opacity: 70%;
    }

    p
    {
        font-size: 1.5rem;
    }

    .list
    {
        padding-top: 1rem;
        padding-bottom: 1rem;
        display: flex;
        flex-wrap: wrap;
        flex-direction: row;
    }

    @media (max-aspect-ratio: 1/1) 
    {
        button
        {
            width: calc(100% - 2rem);
        }
    }
</style>