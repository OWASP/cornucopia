<script>
    import SvelteMarkdown from "svelte-markdown";
    import { newsRenderers } from "$lib/components/renderers/renderers";
    import BlogpostMetadata from "$lib/components/blogpostMetadata.svelte";
    import { readTranslation } from "$lib/stores/stores";
    let t = readTranslation();
    /** @type {{data: any}} */
    let { data } = $props();
    let blogpost = $derived(data.blogpost);
    let markdownRenderers = /** @type {any} */ (newsRenderers);
</script>

<svelte:head>
    <title>{blogpost.title} | OWASP Cornucopia</title>
    <link
        rel="canonical"
        href="https://cornucopia.owasp.org/news/{blogpost.path}"
    />
    <meta
        name="description"
        content={blogpost.markdown
            ?.replace(/[#*_>`]/g, "")
            .replace(/\n+/g, " ")
            .trim()
            .slice(0, 160)}
    />

    <!-- Facebook Meta Tags -->
    <meta
        property="og:url"
        content="https://cornucopia.owasp.org/news/{blogpost.path}"
    />
    <meta property="og:type" content="article" />
    <meta property="og:title" content="{blogpost.title} | OWASP Cornucopia" />
    <meta
        property="og:description"
        content={blogpost.markdown
            ?.replace(/[#*_>`]/g, "")
            .replace(/\n+/g, " ")
            .trim()
            .slice(0, 160)}
    />
    <meta property="og:image" content="/images/opengraph.png" />

    <!-- Twitter Meta Tags -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{blogpost.title} | OWASP Cornucopia" />
    <meta
        name="twitter:description"
        content={blogpost.markdown
            ?.replace(/[#*_>`]/g, "")
            .replace(/\n+/g, " ")
            .trim()
            .slice(0, 160)}
    />
    <meta name="twitter:image" content="/images/opengraph.png" />
</svelte:head>
<div>
    <BlogpostMetadata {blogpost}></BlogpostMetadata>
    <SvelteMarkdown renderers={markdownRenderers} source={blogpost.markdown}
    ></SvelteMarkdown>
    <p>
        <a
            title="OWASP Cornucopia's repository"
            rel="noopener"
            href="https://github.com/OWASP/cornucopia/tree/master/cornucopia.owasp.org/data/news/{blogpost.path}/index.md"
            >{$t("news.slug.p1")}</a
        >
    </p>
</div>

<style>
    p {
        text-align: center;
    }

    @media (max-width: 767px) {
        div {
            margin: 0rem 1rem;
        }
    }
</style>
