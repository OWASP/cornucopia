<script>
    import { goto } from "$app/navigation";
    import { Text } from "$lib/utils/text";
    import SvelteMarkdown from "svelte-markdown";
    import { renderers } from "$lib/components/renderers/renderers";
    import { readLang, readTranslation } from "$lib/stores/stores";

    /** @type {{data: any}} */
    let { data } = $props();
    let t = readTranslation();
    const lang = readLang();
    let content = $derived(data.content.get($lang) || data.content.get("en"));

    function getExcerpt(text, maxLength = 160) {
        if (!text) return "";
        const cleaned = text
            .replace(/[#_*`>]/g, "")
            .replace(/\s+/g, " ")
            .trim();

        return cleaned.length > maxLength
            ? cleaned.slice(0, maxLength) + "…"
            : cleaned;
    }
</script>

<svelte:head>
    <title>{$t("printing.head.title")}</title>
    <link rel="canonical" href="https://cornucopia.owasp.org/news" />
    <meta name="description" content={$t("news.head.description")} />
    <meta name="keywords" content={$t("news.head.keywords")} />
    <meta property="og:title" content={$t("news.head.title")} />``
    <meta property="og:description" content={$t("news.head.description")} />
    <meta name="twitter:title" content={$t("news.head.title")} />
    <meta name="twitter:description" content={$t("news.head.description")} />
</svelte:head>

<div>
    {#if content != ""}
        <SvelteMarkdown {renderers} source={content}></SvelteMarkdown>
    {/if}

    {#if data.posts.length == 0}
        <p>{$t("news.p1")}</p>
    {:else}
        <div class="list">
            {#each data.posts as post}
                <a
                    class="button"
                    title="View {Text.Format(post.path)}"
                    href="/news/{post.path}"
                >
                    <span class="title">{Text.Format(post.title)}</span>

                    <p class="excerpt">
                        {getExcerpt(post.content)}
                    </p>

                    <span class="info">
                        {Text.FormatDate(post.date)}
                        •
                        {Text.Format(post.author)}
                        <span>>> {$t("news.a")}</span>
                    </span>
                </a>
            {/each}
        </div>
    {/if}

    <p>
        {$t("news.p2")}:
        <a
            title="OWASP Cornucopia news author: {$t('news.author.h1')}"
            href="/author">{$t("news.author.h1")}</a
        >
    </p>
</div>

<style>
    a {
        font-weight: bold;
        text-decoration: none;
        transition: var(--transition);
        color: var(--background);
    }

    a:hover {
        opacity: 50%;
    }
    .info {
        font-size: 1rem;
        margin: 1rem;
    }

    .title {
        background-color: rgba(255, 255, 255, 0.237);
        margin: 0;
        padding: 0.5rem;
        border-top-left-radius: 0.5rem;
        border-top-right-radius: 0.5rem;
    }
    .button {
        padding: 1rem;
        width: calc(50% - 4rem);
        margin: 1rem;
        text-align: left;
        font-weight: 400;
        background: none;
        border: none;
        cursor: pointer;
        color: var(--background);
        outline: 1px white solid;
        margin-bottom: 4rem;
        background: white;
        border-radius: 0.5rem;
        transition: var(--transition);
        outline: 1px rgb(231, 231, 231) solid;
        box-shadow: var(--box-shadow);
    }

    .button:hover {
        opacity: 70%;
    }

    .list {
        padding-top: 1rem;
        padding-bottom: 1rem;
        display: flex;
        flex-wrap: wrap;
        flex-direction: row;
    }

    @media (max-aspect-ratio: 1/1) {
        .button {
            width: calc(100% - 2rem);
        }
        div {
            margin: 0rem 1rem;
        }
    }
    .excerpt {
        font-size: 0.95rem;
        line-height: 1.5;
        margin: 0.75rem 0 0.5rem 0;
        color: #333;
    }
</style>
