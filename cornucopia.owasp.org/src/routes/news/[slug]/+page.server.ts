import { LocalCache } from "$lib/utils/cache.js";
import { getBlogpostByTitle } from "../../../domain/blogpost/blogpostController.js";
import { Text } from "$lib/utils/text.js";
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load({ params })
{
    const slug: string = params.slug.toLowerCase();
    const blogpost = await LocalCache(() => getBlogpostByTitle(slug), 20, slug);

    const canonicalUrl = `https://cornucopia.owasp.org/news/${encodeURIComponent(params.slug)}`;

    // Use front-matter description; fall back to body excerpt only when absent
    const excerpt = (blogpost.markdown || '')
        .replace(/[#*_>`]/g, '')
        .replace(/\n+/g, ' ')
        .trim()
        .slice(0, 160);

    const description = blogpost.description || excerpt || 'OWASP Cornucopia news article.';

    // Use front-matter title when present; fall back to description, then slug
    const rawTitle = blogpost.title || blogpost.description || params.slug;
    const title = Text.Format(rawTitle) + ' | OWASP Cornucopia';

    // Normalize tags from front-matter
    const keywords = Array.isArray(blogpost.tags)
        ? blogpost.tags.map((t: string) => t.trim()).filter(Boolean).join(', ')
        : 'OWASP, Cornucopia, news, security';

    const metadata: PageMetadata = {
        title,
        description,
        keywords,
        canonicalUrl,
        type: 'article',
    };

    return { metadata, blogpost };
}