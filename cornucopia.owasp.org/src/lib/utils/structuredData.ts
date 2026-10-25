import type { PageMetadata } from '$lib/types/metadata.js';
import { structuredData as configuredStructuredData } from '$lib/config.js';

export interface StructuredDataConfig {
    website?: Record<string, unknown>;
    product?: Record<string, unknown>;
    organization?: Record<string, unknown>;
}

export const DEFAULT_WEBSITE_NODE: Record<string, unknown> = {
    '@type': 'WebSite',
    '@id': 'https://cornucopia.owasp.org',
    url: 'https://cornucopia.owasp.org',
    name: 'OWASP Cornucopia',
    publisher: { '@id': 'https://owasp.org' },
};

export const DEFAULT_PRODUCT_NODE: Record<string, unknown> = {
    '@type': ['Product', 'Game'],
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

export const DEFAULT_ORGANIZATION_NODE: Record<string, unknown> = {
    '@type': 'Organization',
    '@id': 'https://owasp.org',
    name: 'OWASP Foundation',
    url: 'https://owasp.org',
    logo: 'https://cornucopia.owasp.org/images/owasp-logo.png',
};

export const loadStructuredDataConfig = (
    source: unknown = configuredStructuredData,
): StructuredDataConfig => {
    return (source as StructuredDataConfig) ?? {};
};

export const generateStructuredData = (
    metadata: PageMetadata,
    configOverride?: StructuredDataConfig,
): Record<string, unknown> => {
    if (metadata.structuredData) {
        return metadata.structuredData;
    }

    const config = configOverride ?? loadStructuredDataConfig();

    const normalizedUrl = metadata.canonicalUrl
        ? metadata.canonicalUrl.trim().replace(/\/+$/, '')
        : '';
    const isHome = !normalizedUrl || normalizedUrl === 'https://cornucopia.owasp.org';

    const webSiteNode: Record<string, unknown> = config.website
        ? { ...config.website }
        : { ...DEFAULT_WEBSITE_NODE };

    const productNode: Record<string, unknown> = config.product
        ? { ...config.product }
        : { ...DEFAULT_PRODUCT_NODE };

    const organizationNode: Record<string, unknown> = config.organization
        ? { ...config.organization }
        : { ...DEFAULT_ORGANIZATION_NODE };

    const siteId =
        (typeof webSiteNode['@id'] === 'string' && webSiteNode['@id']) ||
        'https://cornucopia.owasp.org';

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
            isPartOf: { '@id': siteId },
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
