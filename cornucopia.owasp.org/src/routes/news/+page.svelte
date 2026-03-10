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
    function getExcerpt(markdown) {
        if (!markdown) return "";

        return (
            markdown
                .replace(/!\[.*?\]\(.*?\)/g, "") // remove images
                .replace(/[#*_>`]/g, "")
                .replace(/\n+/g, " ")
                .trim()
                .slice(0, 160) + "..."
        );
    }
    let groupedList = $derived(
        Object.entries(
            (data?.posts ?? []).reduce((groups, post) => {
                const year = String(post?.date ?? "").slice(0, 4);
                if (!groups[year]) groups[year] = [];
                groups[year].push(post);
                return groups;
            }, {}),
        )
            .sort(([a], [b]) => Number(b) - Number(a))
            .map(([year, posts]) => ({ year, posts })),
    );
    function extractFirstImage(markdown) {
        const match = markdown?.match(/!\[.*?\]\((.*?)\)/);
        if (!match) return null;

        const filename = match[1].split("/").pop();
        return `/images/${filename}`;
    }
    let authorMap = $derived(() => {
        const list = data?.authors ?? [];
        const map = {};

        for (const author of list) {
            map[author.id] = author; // or author.name depending on structure
        }
        return map;
    });
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
    {#each groupedList as group}
        <h2 class="year-heading">{group.year}</h2>
        <hr class="year-divider" />
        <div class="list">
            {#each group.posts as post}
                {@const image = extractFirstImage(post.markdown)}
                <a class="button" href="/news/{post.path}">
                    <div class="card-header">
                        <img
                            src={`/images/authors/${post.author
                                .toLowerCase()
                                .replace(/\s+/g, "-")}.jpg`}
                            alt={post.author}
                            class="card-image"
                        />
                        <div class="card-text">
                            <span class="title">{Text.Format(post.title)}</span>
                            <span class="meta">
                                {Text.FormatDate(post.date)} • {post.author}
                            </span>
                            <span class="readmore">Read more →</span>
                        </div>
                    </div>
                </a>
            {/each}
        </div>
    {/each}
    <p>
        {$t("news.p2")}:
        <a
            title="OWASP Cornucopia news author: {$t('news.author.h1')}"
            href="/author"
        >
            {$t("news.author.h1")}
        </a>
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
        font-size: 0.8rem;
        color: #777;
        margin-top: 0.75rem;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    .meta-left {
        white-space: nowrap;
    }
    .readmore {
        font-size: 0.85rem;
        font-weight: 500;
        margin-top: 0.4rem;
        color: #1f3b63;
        transition: all 0.2s ease;
    }
    .title {
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
        padding: 0;
        background: none;
    }
    .button {
        padding: 1.4rem;
        background: white;
        border-radius: 0.9rem;
        text-decoration: none;
        color: inherit;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
        transition: all 0.25s ease;
        display: block;
        transform: translateY(-4px);
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.08);
    }
    .button:hover .readmore {
        transform: translateX(4px);
    }

    .title {
        font-size: 1.05rem;
        font-weight: 600;
        line-height: 1.35;
    }
    .excerpt {
        font-size: 0.9rem;
        line-height: 1.6;
        color: #555;
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
        display: block;
    }
    .year-heading {
        margin-top: 3rem;
        font-size: 1.75rem;
        font-weight: 700;
    }
    .year-divider {
        margin: 0.5rem 0 1.5rem 0;
        border: none;
        border-top: 1px solid #ddd;
    }
    .author {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .avatar {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        object-fit: cover;
    }
    .card-image {
        width: 56px;
        height: 56px;
        object-fit: cover;
        border-radius: 50%;
        flex-shrink: 0;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
    }
    .list {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 2rem;
        align-items: stretch;
    }
    .card-header {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    @media (max-aspect-ratio: 1/1) {
        div {
            margin: 0 1rem;
        }
        
        .year-heading {
            margin-left: 1rem;
            margin-right: 1rem;
        }
        
        .year-divider {
            margin-left: 1rem;
            margin-right: 1rem;
        }
        
        .list {
            margin: 0 1rem;
        }
    }
</style>
