<script lang="ts">
    import { goto } from "$app/navigation";
    import { Text } from "$lib/utils/text";
    import type { Blogpost } from "../../domain/blogpost/blogpost";

    interface Props {
        blogpost: Blogpost;
    }

    let { blogpost }: Props = $props();

    let authorLink = $derived("/author/" + blogpost.author);
</script>

<div class="metadata">
    <div class="left">
        <p>Date: {Text.FormatDate(blogpost.date)}</p>
        <p>
            Author:
            <a href={authorLink}>{Text.Format(blogpost.author)}</a>
        </p>
        <div class="tags">
            <span class="tags-label">Tags:</span>
            <div class="tags-container">
                {#each blogpost.tags || [] as tag}
                    <a
                        title={`OWASP Cornucopia new post titled: ${Text.Format(tag)}`}
                        class="tag"
                        href="/news"
                    >
                        {Text.Format(tag)}
                    </a>
                {/each}
            </div>
        </div>
    </div>
    <div class="right">
        <button onclick={() => goto(authorLink)}>
            <img
                title={`OWASP Cornucopia news author ${Text.Format(blogpost.author)}`}
                alt={`${blogpost.author} profile picture`}
                src={`/data/author/${blogpost.author}/profile-picture.jpg`}
            />
        </button>
    </div>
</div>

<style>
    .tag {
        padding: 0.25rem 0.5rem;
        color: var(--background);
        background-color: var(--white);
        text-decoration: none;
        border-radius: 4px;
    }

    .tag:hover {
        opacity: 70%;
    }

    .metadata {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 1rem;
        padding-bottom: 2rem;
    }

    .left {
        flex: 1;
        min-width: 1rem;
    }

    .right {
        flex-shrink: 0;
        display: flex;
        align-items: flex-start; /* important */
        justify-content: flex-end;
        margin-top: 1rem;
    }

    img {
        width: 6rem;
        height: 6rem;
        object-fit: cover;
        border-radius: 50%;
        outline: 1px white solid;
        cursor: pointer;
        margin-top: 0; /* remove vertical offset */
    }

    .img:hover {
        opacity: 70%;
    }

    .button {
        background: none;
        border: none;
    }
    .tags {
        margin-top: 0.5rem;
    }

    .tags-label {
        display: block;
        margin-bottom: 0.25rem;
    }

    .tags-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
</style>
