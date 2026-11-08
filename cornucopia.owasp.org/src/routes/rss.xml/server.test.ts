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

    it('does not append an ellipsis to a description that is already short', async () => {
        getBlogposts.mockReturnValue([createPost({ description: 'A short description' })]);

        const response = await GET();
        const body = await response.text();

        expect(body).toContain('<description>A short description</description>');
    });

    it('keeps a description of exactly 200 characters unchanged', async () => {
        const description = 'A'.repeat(200);
        getBlogposts.mockReturnValue([createPost({ description })]);

        const response = await GET();
        const body = await response.text();

        expect(body).toContain(`<description>${description}</description>`);
    });

    it('truncates a longer description and marks it with an ellipsis', async () => {
        const description = 'A'.repeat(200) + 'B';
        getBlogposts.mockReturnValue([createPost({ description })]);

        const response = await GET();
        const body = await response.text();

        expect(body).toContain(`<description>${'A'.repeat(200)}...</description>`);
        expect(body).not.toContain(description);
    });

    it('renders an empty description when the blogpost has none', async () => {
        getBlogposts.mockReturnValue([createPost({ description: undefined })]);

        const response = await GET();
        const body = await response.text();

        expect(body).toContain('<description></description>');
    });
});