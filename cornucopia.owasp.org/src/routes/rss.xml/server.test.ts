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

describe('GET /rss.xml', () => {
    beforeEach(() => {
        getBlogposts.mockReturnValue([
            {
                title: 'Test post',
                path: 'test-post',
                author: 'test-author',
                markdown: '',
                tags: ['test'],
                hidden: false,
                date: '20231201',
                description: 'A test post',
            },
        ]);
    });

    it('renders a valid RFC 822 pubDate', async () => {
        const response = await GET();
        const body = await response.text();

        expect(body).toContain('<pubDate>Fri, 01 Dec 2023 00:00:00 GMT</pubDate>');
    });
});
