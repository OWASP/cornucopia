import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper.js';
import { LocalCache } from '$lib/utils/cache.js';
import { getAuthors } from '../../domain/author/authorController.js';
import { getBlogposts } from '../../domain/blogpost/blogpostController.js';
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load(event)
{
    const t = event.locals.translation;
    const fb = event.locals.fallbackTranslation;
    const metadata: PageMetadata = {
        title: t?.news?.head?.title ?? fb?.news?.head?.title ?? 'OWASP Cornucopia - News',
        description: t?.news?.head?.description ?? fb?.news?.head?.description ?? '',
        keywords: t?.news?.head?.keywords ?? fb?.news?.head?.keywords ?? '',
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