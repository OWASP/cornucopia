<script>
    import { Text } from "$lib/utils/text";
    import SvelteMarkdown from "svelte-markdown";
    /** @type {{data: any}} */
    let { data } = $props();
</script>
<svelte:head>
    <link rel="canonical" href="/author" />
        <title>OWASP Cornucopia - {data.author.name}</title>
        <meta name="description" content="OWASP Cornucopia - {data.author.name}" />
        <meta name="keywords" content="OWASP, Cornucopia, {data.author.name}" />
        <meta property="og:title" content="OWASP Cornucopia - {data.author.name}">
        <meta property="og:description" content="OWASP Cornucopia - {data.author.name}">
        <meta name="twitter:title" content="OWASP Cornucopia - {data.author.name}">
        <meta name="twitter:description" content="OWASP Cornucopia - {data.author.name}">
</svelte:head>
<div>
<div class="container">
    <div class="left">
        <img class="profile-picture" alt="OWASP Cornucopia - {data.author.name}" title="OWASP Cornucopia new author: {data.author.name}" src="/data/author/{data.author.name}/profile-picture.jpg"/>
    </div>
    <div class="right">
        <table>
            <tbody>
            {#if data.author.linkedin}
            <tr>
                <td>
                    <img alt="linkedin logo" title="linkedin logo" class="icon" src="/icons/linkedin.png"/>
                </td>
                <td>
                    <a target="_blank" rel="noopener" href="{data.author.linkedin}">LinkedIn</a>
                </td>
            </tr>
            {/if}

            {#if data.author.email}
            <tr>
                <td>
                    <img alt="email logo" title="email logo" class="icon" src="/icons/mail.png"/>
                </td>
                <td>
                    <a target="_blank" rel="noopener" href="mailto:{data.author.email}">Mail</a>
                </td>
            </tr>
            {/if}

            {#if data.author.website}
            <tr>
                <td>
                    <img alt="globe logo" title="globe logo" class="icon" src="/icons/globe.png"/>
                </td>
                <td>
                    <a target="_blank" rel="noopener" href="{data.author.website}">{Text.DisplayLink(data.author.website)}</a>
                </td>
            </tr>
            {/if}
            </tbody>
        </table>

    </div>
</div>

<SvelteMarkdown source={data.author.bio}></SvelteMarkdown>
<h2>All blogposts by this author:</h2>
    {#if data.blogposts.length == 0}
        <p>This author didn't publish yet</p>
    {:else}
        <ul>
            {#each data.blogposts as blogpost}
                <li>
                    <a href="/news/{blogpost.path}">{Text.Format(blogpost.title)}</a>
                </li>
            {/each}
        </ul>
    {/if}
</div>
<style>
    .container
    {
        display: flex;
        flex-direction: row;
    }

    .icon
    {
        width : 1rem;
    }

    .profile-picture
    {
        display: block;
        width : 10rem;
        margin:auto;
        outline: 1px white solid
    }

    table
    {
        margin-left: 1rem;
    }
    @media (max-aspect-ratio: 1/1) 
    {
        .container
        {
            margin: auto;
        }
        div
        {
            margin: 0rem 1rem;
        }
    }
</style>