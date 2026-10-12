import type { PageMetadata } from "$lib/types/metadata.js";

export function load()
{
    const metadata: PageMetadata = {
        title: '404 Not Found | OWASP Cornucopia',
        description: 'The page you requested could not be found.',
        keywords: 'OWASP, Cornucopia, 404, not found',
        canonicalUrl: 'https://cornucopia.owasp.org/404',
        type: 'website',
    };
    return { metadata };
}