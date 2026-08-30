import { getAuthors } from '../../domain/author/authorController.js';
import type { PageMetadata } from "$lib/types/metadata.js";

export function load(event)
{
    const t = event.locals.translation;
    const fb = event.locals.fallbackTranslation;
    const metadata: PageMetadata = {
        title: t?.author?.head?.title ?? fb?.author?.head?.title ?? 'OWASP Cornucopia - News Authors',
        description: t?.author?.head?.description ?? fb?.author?.head?.description ?? '',
        keywords: t?.author?.head?.keywords ?? fb?.author?.head?.keywords ?? '',
        canonicalUrl: 'https://cornucopia.owasp.org/author',
        type: 'website',
    };
    return { metadata, authors: getAuthors() };
}