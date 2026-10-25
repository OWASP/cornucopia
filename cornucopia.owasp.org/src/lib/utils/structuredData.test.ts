import { describe, it, expect } from 'vitest';
import type { PageMetadata } from '$lib/types/metadata.js';
import {
    generateStructuredData,
    serializeJsonLd,
    loadStructuredDataConfig,
    DEFAULT_WEBSITE_NODE,
    DEFAULT_PRODUCT_NODE,
    DEFAULT_ORGANIZATION_NODE,
} from './structuredData.js';

describe('generateStructuredData', () => {
    it('returns WebSite, Product, and Organization for home page', () => {
        const metadata: PageMetadata = {
            title: 'OWASP Cornucopia - Threat modeling for everyone',
            description: 'OWASP Cornucopia card game description',
            keywords: 'OWASP, Cornucopia',
            canonicalUrl: 'https://cornucopia.owasp.org',
        };

        const result = generateStructuredData(metadata);
        expect(result['@context']).toBe('https://schema.org');

        const graph = result['@graph'] as Record<string, unknown>[];
        expect(graph).toHaveLength(3);

        const [website, product, organization] = graph;
        expect(website['@type']).toBe('WebSite');
        expect(website['@id']).toBe('https://cornucopia.owasp.org');
        expect(website['url']).toBe('https://cornucopia.owasp.org');
        expect(website['name']).toBe('OWASP Cornucopia');
        expect(website['publisher']).toEqual({ '@id': 'https://owasp.org' });

        expect(product['@type']).toEqual(['Product', 'Game']);
        expect(product['@id']).toBe('https://cornucopia.owasp.org#product');
        expect(product['name']).toBe('OWASP Cornucopia Card Game');
        expect(product['brand']).toEqual({ '@id': 'https://owasp.org' });
        expect(product['license']).toBe(
            'https://github.com/OWASP/cornucopia/blob/master/LICENSE.md',
        );
        expect(product['offers']).toEqual({
            '@type': 'Offer',
            price: '0.00',
            priceCurrency: 'USD',
            availability: 'https://schema.org/InStock',
        });

        expect(organization['@type']).toBe('Organization');
        expect(organization['@id']).toBe('https://owasp.org');
        expect(organization['name']).toBe('OWASP Foundation');
        expect(organization['url']).toBe('https://owasp.org');
        expect(organization['logo']).toBe(
            'https://cornucopia.owasp.org/images/owasp-logo.png',
        );
    });

    it('treats root URL with trailing slash as home page', () => {
        const metadata: PageMetadata = {
            title: 'OWASP Cornucopia',
            description: 'Home',
            keywords: 'OWASP',
            canonicalUrl: 'https://cornucopia.owasp.org/',
        };

        const result = generateStructuredData(metadata);
        const graph = result['@graph'] as Record<string, unknown>[];
        expect(graph).toHaveLength(3);
        expect(graph[0]['@type']).toBe('WebSite');
    });

    it('treats empty canonicalUrl as home page', () => {
        const metadata: PageMetadata = {
            title: 'OWASP Cornucopia',
            description: 'Home',
            keywords: 'OWASP',
            canonicalUrl: '',
        };

        const result = generateStructuredData(metadata);
        const graph = result['@graph'] as Record<string, unknown>[];
        expect(graph).toHaveLength(3);
        expect(graph[0]['@type']).toBe('WebSite');
    });

    it('adds a unique WebPage node for subpages', () => {
        const metadata: PageMetadata = {
            title: 'About - OWASP Cornucopia',
            description: 'Learn about Cornucopia',
            keywords: 'about, cornucopia',
            canonicalUrl: 'https://cornucopia.owasp.org/about',
            imageUrl: 'https://cornucopia.owasp.org/images/about.png',
        };

        const result = generateStructuredData(metadata);
        const graph = result['@graph'] as Record<string, unknown>[];
        expect(graph).toHaveLength(4);

        const pageNode = graph[0];
        expect(pageNode['@type']).toBe('WebPage');
        expect(pageNode['@id']).toBe('https://cornucopia.owasp.org/about');
        expect(pageNode['url']).toBe('https://cornucopia.owasp.org/about');
        expect(pageNode['name']).toBe('About - OWASP Cornucopia');
        expect(pageNode['description']).toBe('Learn about Cornucopia');
        expect(pageNode['image']).toBe('https://cornucopia.owasp.org/images/about.png');
        expect(pageNode['isPartOf']).toEqual({ '@id': 'https://cornucopia.owasp.org' });

        expect(graph[1]['@type']).toBe('WebSite');
        expect(graph[2]['@type']).toEqual(['Product', 'Game']);
        expect(graph[3]['@type']).toBe('Organization');
    });

    it('uses Article type when metadata.type is article', () => {
        const metadata: PageMetadata = {
            title: 'News Article Title',
            description: 'Article description',
            keywords: 'news, release',
            canonicalUrl: 'https://cornucopia.owasp.org/news/2026-update',
            type: 'article',
        };

        const result = generateStructuredData(metadata);
        const graph = result['@graph'] as Record<string, unknown>[];
        expect(graph[0]['@type']).toBe('Article');
        expect(graph[0]['name']).toBe('News Article Title');
    });

    it('returns custom structuredData if supplied in metadata', () => {
        const customData = {
            '@context': 'https://schema.org',
            '@type': 'CustomType',
            customField: 'value',
        };
        const metadata: PageMetadata = {
            title: 'Custom',
            description: 'Custom',
            keywords: 'custom',
            canonicalUrl: 'https://cornucopia.owasp.org/custom',
            structuredData: customData,
        };

        const result = generateStructuredData(metadata);
        expect(result).toBe(customData);
    });

    it('generates distinct WebPage nodes for distinct subpages', () => {
        const page1: PageMetadata = {
            title: 'About',
            description: 'About us',
            keywords: 'about',
            canonicalUrl: 'https://cornucopia.owasp.org/about',
        };
        const page2: PageMetadata = {
            title: 'News',
            description: 'Latest news',
            keywords: 'news',
            canonicalUrl: 'https://cornucopia.owasp.org/news',
        };

        const result1 = generateStructuredData(page1);
        const result2 = generateStructuredData(page2);

        const graph1 = result1['@graph'] as Record<string, unknown>[];
        const graph2 = result2['@graph'] as Record<string, unknown>[];

        expect(graph1[0]['@id']).toBe('https://cornucopia.owasp.org/about');
        expect(graph2[0]['@id']).toBe('https://cornucopia.owasp.org/news');
        expect(graph1[0]['@id']).not.toBe(graph2[0]['@id']);
    });

    it('loads configured nodes from configOverride when provided', () => {
        const customConfig = {
            website: {
                '@type': 'WebSite',
                '@id': 'https://custom.example.org',
                url: 'https://custom.example.org',
                name: 'Custom Cornucopia',
            },
            product: {
                '@type': ['Product', 'Game'],
                '@id': 'https://custom.example.org#product',
                name: 'Custom Game',
            },
            organization: {
                '@type': 'Organization',
                '@id': 'https://custom-org.example.org',
                name: 'Custom Org',
            },
        };

        const metadata: PageMetadata = {
            title: 'Subpage',
            description: 'Subpage desc',
            keywords: 'test',
            canonicalUrl: 'https://custom.example.org/test',
        };

        const result = generateStructuredData(metadata, customConfig);
        const graph = result['@graph'] as Record<string, unknown>[];

        expect(graph).toHaveLength(4);
        expect(graph[0]['isPartOf']).toEqual({ '@id': 'https://custom.example.org' });
        expect(graph[1]['name']).toBe('Custom Cornucopia');
        expect(graph[2]['name']).toBe('Custom Game');
        expect(graph[3]['name']).toBe('Custom Org');
    });

    it('falls back to default nodes if empty config is provided', () => {
        const metadata: PageMetadata = {
            title: 'Home',
            description: 'Home desc',
            keywords: 'test',
            canonicalUrl: 'https://cornucopia.owasp.org',
        };

        const result = generateStructuredData(metadata, {});
        const graph = result['@graph'] as Record<string, unknown>[];

        expect(graph[0]).toEqual(DEFAULT_WEBSITE_NODE);
        expect(graph[1]).toEqual(DEFAULT_PRODUCT_NODE);
        expect(graph[2]).toEqual(DEFAULT_ORGANIZATION_NODE);
    });

    it('loadStructuredDataConfig returns an object and handles null source', () => {
        const config = loadStructuredDataConfig();
        expect(typeof config).toBe('object');
        const fallbackConfig = loadStructuredDataConfig(null as any);
        expect(fallbackConfig).toEqual({});
    });

    it('uses fallback siteId if website @id is not a string', () => {
        const metadata: PageMetadata = {
            title: 'Subpage',
            description: 'Subpage desc',
            keywords: 'test',
            canonicalUrl: 'https://cornucopia.owasp.org/test',
        };

        const result = generateStructuredData(metadata, {
            website: { '@type': 'WebSite' },
        });
        const graph = result['@graph'] as Record<string, unknown>[];
        expect(graph[0]['isPartOf']).toEqual({ '@id': 'https://cornucopia.owasp.org' });
    });
});

describe('serializeJsonLd', () => {
    it('serializes JSON and wraps it in a script tag', () => {
        const data = {
            '@context': 'https://schema.org',
            name: 'OWASP Cornucopia',
        };

        const output = serializeJsonLd(data);
        expect(output.startsWith('<script type="application/ld+json">')).toBe(true);
        expect(output.endsWith('</script>')).toBe(true);

        const innerJson = output
            .replace('<script type="application/ld+json">', '')
            .replace('</script>', '');
        const parsed = JSON.parse(innerJson);
        expect(parsed).toEqual(data);
    });

    it('escapes < characters to prevent script injection / premature closure', () => {
        const data = {
            description: '</script><script>alert("xss")</script>',
        };

        const output = serializeJsonLd(data);
        expect(output).not.toContain('</script><script>');
        expect(output).toContain('\\u003c/script>\\u003cscript>');

        const innerJson = output
            .replace('<script type="application/ld+json">', '')
            .replace('</script>', '');
        const parsed = JSON.parse(innerJson);
        expect(parsed.description).toBe('</script><script>alert("xss")</script>');
    });
});
