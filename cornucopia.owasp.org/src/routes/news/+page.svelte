<script>
    import { goto } from '$app/navigation';
    import { Text } from '$lib/utils/text';
    import SvelteMarkdown from 'svelte-markdown';
    import renderers from '$lib/components/renderers/renderers';
    import {readLang, readTranslation} from "$lib/stores/stores";

    /** @type {{data: any}} */
    let { data } = $props();
    let t = readTranslation();
    const lang = readLang();
    let content = data.content.get($lang) || data.content.get('en');
</script>
<div>
{#if content != ''}
<SvelteMarkdown {renderers} source={content}></SvelteMarkdown>
{/if}

{#if data.posts.length == 0}
<p>{$t('news.p1')}</p>
{:else}
    <div class="list">
        {#each data.posts as post}
            <button title="View {Text.Format(post.path)}" onclick={()=>goto('/news/' + post.path)}>
                <p class="title">{Text.Format(post.title)}</p>
                <p class="info">
                    {Text.FormatDate(post.date)}
                     • 
                    {Text.Format(post.author)}
                    <a href="/news/{post.path}">>> {$t('news.a')}</a>
                </p>
            </button>
        {/each}
    </div>
{/if}


<p>{$t('news.p2')} <a href="/author">{$t('news.slug.p1')}</a></p>
{#each data.authors as author}
    <p>
        <a href="/author/{author.name}">{author.name}</a>
    </p>
{/each}
</div>
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
        box-shadow: var(--box-shadow);
    }

    button:hover
    {
        opacity: 70%;
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
        div
        {
            margin: 0rem 1rem;
        }
    }
</style>