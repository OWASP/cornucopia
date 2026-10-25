import type { PageMetadata } from '$lib/types/metadata.js';

export const generateStructuredData = (
    metadata: PageMetadata,
): Record<string, unknown> => {
    if (metadata.structuredData) {
        return metadata.structuredData;
    }

    const normalizedUrl = metadata.canonicalUrl
        ? metadata.canonicalUrl.trim().replace(/\/+$/, '')
        : '';
    const isHome = !normalizedUrl || normalizedUrl === 'https://cornucopia.owasp.org';

    const webSiteNode: Record<string, unknown> = {
        '@type': 'WebSite',
        '@id': 'https://cornucopia.owasp.org',
        url: 'https://cornucopia.owasp.org',
        name: 'OWASP Cornucopia',
        publisher: { '@id': 'https://owasp.org' },
    };

    const productNode: Record<string, unknown> = {
        '@type': 'Product',
        '@id': 'https://cornucopia.owasp.org#product',
        name: 'OWASP Cornucopia Card Game',
        description:
            'An open-source card game to assist software development teams identify security requirements and map threat modeling.',
        brand: { '@id': 'https://owasp.org' },
        license:
            'https://github.com/OWASP/cornucopia/blob/master/LICENSE.md',
        offers: {
            '@type': 'Offer',
            price: '0.00',
            priceCurrency: 'USD',
            availability: 'https://schema.org/InStock',
        },
    };

    const organizationNode: Record<string, unknown> = {
        '@type': 'Organization',
        '@id': 'https://owasp.org',
        name: 'OWASP Foundation',
        url: 'https://owasp.org',
        logo: 'https://cornucopia.owasp.org/images/owasp-logo.png',
    };

    const graph: Record<string, unknown>[] = [
        webSiteNode,
        productNode,
        organizationNode,
    ];

    if (!isHome) {
        const pageType = metadata.type === 'article' ? 'Article' : 'WebPage';
        const pageNode: Record<string, unknown> = {
            '@type': pageType,
            '@id': metadata.canonicalUrl,
            url: metadata.canonicalUrl,
            name: metadata.title,
            description: metadata.description,
            isPartOf: { '@id': 'https://cornucopia.owasp.org' },
        };
        if (metadata.imageUrl) {
            pageNode.image = metadata.imageUrl;
        }
        graph.unshift(pageNode);
    }

    return {
        '@context': 'https://schema.org',
        '@graph': graph,
    };
};

export const serializeJsonLd = (data: Record<string, unknown>): string => {
    const json = JSON.stringify(data).replace(/</g, '\\u003c');
    return `<script type="application/ld+json">${json}</script>`;
};
