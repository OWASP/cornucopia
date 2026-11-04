import { describe, it, expect, vi, beforeEach } from 'vitest';

const { getBlogposts } = vi.hoisted(() => ({
    getBlogposts: vi.fn(),
}));

vi.mock('../../domain/blogpost/blogpostController.js', () => ({
    getBlogposts,
}));

vi.mock('$lib/utils/cache.js', () => ({
    LocalCache: vi.fn(async (load: () => unknown) => load()),
}));

vi.mock('$lib/utils/text.js', () => ({
    Text: {
        Format: (value: string) => value,
    },
}));

import { GET } from './+server';

const createPost = (overrides: Record<string, unknown> = {}) => ({
    title: 'Test post',
    path: 'test-post',
    author: 'test-author',
    markdown: '',
    tags: ['test'],
    hidden: false,
    date: '20231201',
    description: 'A test post',
    ...overrides,
});

describe('GET /rss.xml', () => {
    beforeEach(() => {
        getBlogposts.mockReturnValue([createPost()]);
    });

    it('points the item source at the published RSS feed', async () => {
        const response = await GET();
        const body = await response.text();

        expect(body).toContain('<source url="https://cornucopia.owasp.org/rss.xml">');
        expect(body).not.toContain('<source url="https://cornucopia.owasp.org/rss">');
    });

    it('uses the standard s-maxage Cache-Control directive', async () => {
        const response = await GET();
        const cacheControl = response.headers.get('Cache-Control');

        expect(cacheControl).toContain('s-maxage=600');
        expect(cacheControl).not.toContain('s-max-age');
    });
});