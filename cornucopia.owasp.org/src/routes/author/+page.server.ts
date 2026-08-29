import { getAuthors } from '../../domain/author/authorController.js';
import type { PageMetadata } from "$lib/types/metadata.js";

export function load({ params: _params })
{
    const metadata: PageMetadata = {
        title: 'Authors | OWASP Cornucopia',
        description: 'Meet the authors and contributors behind OWASP Cornucopia.',
        keywords: 'OWASP, Cornucopia, authors, contributors',
        canonicalUrl: 'https://cornucopia.owasp.org/author',
        type: 'website',
    };
    return { metadata, authors: getAuthors() };
}