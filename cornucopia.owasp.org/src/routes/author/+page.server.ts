import { getPageMetadata } from '$lib/utils/pageMetadata.js';
import { getAuthors } from '../../domain/author/authorController.js';

export function load(event)
{
    const metadata = getPageMetadata(event, 'author', 'https://cornucopia.owasp.org/author');
    return { metadata, authors: getAuthors() };
}