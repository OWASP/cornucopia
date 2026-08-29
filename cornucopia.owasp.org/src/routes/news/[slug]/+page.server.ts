import { LocalCache } from "$lib/utils/cache.js";
import { getBlogpostByTitle } from "../../../domain/blogpost/blogpostController.js";
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load({ params })
{
    const title: string = params.slug.toLowerCase();
    const blogpost = await LocalCache(() => getBlogpostByTitle(title), 20, title);

    const excerpt = (blogpost.markdown || '')
        .replace(/[#*_>`]/g, '')
        .replace(/\n+/g, ' ')
        .trim()
        .slice(0, 160);

    const metadata: PageMetadata = {
        title: blogpost.title ? `${blogpost.title} | OWASP Cornucopia` : 'News | OWASP Cornucopia',
        description: excerpt || 'OWASP Cornucopia news article.',
        keywords: 'OWASP, Cornucopia, news, security',
        canonicalUrl: `https://cornucopia.owasp.org/news/${encodeURIComponent(blogpost.path)}`,
        type: 'article',
    };

    return { metadata, blogpost };
}