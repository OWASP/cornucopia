<script>
    import { goto } from "$app/navigation";
    import { Text } from "$lib/utils/text";
    import SvelteMarkdown from "svelte-markdown";
    import { renderers } from "$lib/components/renderers/renderers";
    import { readLang, readTranslation } from "$lib/stores/stores";

    /** @type {{data: any}} */
    let { data } = $props();
    let t = readTranslation();
    const langStore = readLang();
    let content = $derived(
        data?.content?.get($langStore) || data?.content?.get("en") || "",
    );

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
    let sortedPosts = $derived(
        Array.isArray(data?.posts)
            ? [...data.posts].sort((a, b) => {
                  const dateA = new Date(a?.date || 0);
                  const dateB = new Date(b?.date || 0);
                  return dateB - dateA;
              })
            : [],
    );
</script>

<svelte:head>
    <title>{$t("printing.head.title")}</title>
    <link rel="canonical" href="https://cornucopia.owasp.org/news" />
    <meta name="description" content={$t("news.head.description")} />
    <meta name="keywords" content={$t("news.head.keywords")} />
    <meta property="og:title" content={$t("news.head.title")} />
    <meta property="og:description" content={$t("news.head.description")} />
    <meta name="twitter:title" content={$t("news.head.title")} />
    <meta name="twitter:description" content={$t("news.head.description")} />
</svelte:head>

<div>
    {#if content != ""}
        <SvelteMarkdown {renderers} source={content}></SvelteMarkdown>
    {/if}

    {#if !data?.posts || data.posts.length === 0}
        <p>{$t("news.p1")}</p>
    {:else}
        <div class="list">
            {#each sortedPosts as post}
                <a
                    class="button"
                    title="View {Text.Format(post.path)}"
                    href="/news/{post.path}"
                >
                    <span class="title">{Text.Format(post.title)}</span>

                    <p class="excerpt">
                        {getExcerpt(post.content)}
                    </p>

                    <div class="meta">
                        <span class="meta-left">
                            {Text.FormatDate(post.date)} • {Text.Format(
                                post.author,
                            )}
                        </span>
                        <span class="readmore">{$t("news.a")} →</span>
                    </div>
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
        opacity: 70%;
    }
    .meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.85rem;
        color: #666;
        margin-top: 0.75rem;
        gap: 0.5rem;
        flex-wrap: wrap;
    }

    .meta-left {
        white-space: nowrap;
    }

    .readmore {
        font-weight: 500;
    }
    .title {
        font-size: 1.15rem;
        font-weight: 600;
        margin: 0 0 0.75rem 0;
        padding: 0;
        background: none;
    }

    .button {
        padding: 1rem;
        margin: 1rem;
        text-align: left;
        font-weight: 400;
        background: none;
        border: none;
        cursor: pointer;
        color: var(--background);
        background: white;
        border-radius: 0.5rem;
        transition: var(--transition);
        outline: 1px rgb(231, 231, 231) solid;
        box-shadow: var(--box-shadow);
    }
    .button:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
    }

    .list {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
    }

    .excerpt {
        font-size: 0.95rem;
        line-height: 1.6;
        color: #444;
        margin: 0 0 0.75rem 0;
    }
    .card {
        padding: 1.5rem;
        background: white;
        border-radius: 0.75rem;
        box-shadow: var(--box-shadow);
        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
        text-decoration: none;
        color: inherit;
        display: flex;
        flex-direction: column;
    }
</style>
