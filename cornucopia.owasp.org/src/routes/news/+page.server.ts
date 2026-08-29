import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper.js';
import { LocalCache } from '$lib/utils/cache.js';
import { getAuthors } from '../../domain/author/authorController.js';
import { getBlogposts } from '../../domain/blogpost/blogpostController.js';
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load({ params: _params })
{
    const metadata: PageMetadata = {
        title: 'News | OWASP Cornucopia',
        description: 'Latest news, updates and blog posts from the OWASP Cornucopia project.',
        keywords: 'OWASP, Cornucopia, news, blog, updates',
        canonicalUrl: 'https://cornucopia.owasp.org/news',
        type: 'website',
    };
    return {
        metadata,
        content: FileSystemHelper.getDataFromPath('data/website/pages/news'),
        posts: await LocalCache(() => getBlogposts(), 20, 'posts'),
        authors: await LocalCache(() => getAuthors(), 20, 'authors'),
    };
}