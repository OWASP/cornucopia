import { getAuthor } from "../../../domain/author/authorController.js";
import { getBlogpostsByAuthor } from "../../../domain/blogpost/blogpostController.js";
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load({ params })
{
    const author = getAuthor(params.name);
    const metadata: PageMetadata = {
        title: `OWASP Cornucopia - ${author.name}`,
        description: `OWASP Cornucopia - ${author.name}`,
        keywords: `OWASP, Cornucopia, ${author.name}`,
        canonicalUrl: `https://cornucopia.owasp.org/author/${encodeURIComponent(params.name)}`,
        type: 'website',
    };
    return {
        metadata,
        author,
        blogposts: getBlogpostsByAuthor(params.name)
    };
}