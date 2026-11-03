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

const unescapedAmpersand = /&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)/;

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

describe('GET /rss.xml XML escaping', () => {
    beforeEach(() => {
        getBlogposts.mockReturnValue([createPost()]);
    });

    it('escapes special characters in every dynamic RSS field', async () => {
        getBlogposts.mockReturnValue([
            createPost({
                title: 'Research & Development <2026>',
                path: 'research?a=1&b=2',
                tags: ['tips & tricks', '<security>', "O'Reilly"],
                description: 'A & B <script> "quoted"',
            }),
        ]);

        const response = await GET();
        const body = await response.text();

        expect(body).toContain('<title>Research &amp; Development &lt;2026&gt;</title>');
        expect(body).toContain('<link>https://cornucopia.owasp.org/news/research?a=1&amp;b=2</link>');
        expect(body).toContain('<description>A &amp; B &lt;script&gt; &quot;quoted&quot;...</description>');
        expect(body).toContain(
            '<guid isPermaLink="true">https://cornucopia.owasp.org/news/research?a=1&amp;b=2</guid>'
        );
        expect(body).toContain('<category>tips &amp; tricks</category>');
        expect(body).toContain('<category>&lt;security&gt;</category>');
        expect(body).toContain('<category>O&apos;Reilly</category>');
        expect(body).not.toMatch(unescapedAmpersand);
    });

    it('escapes the ampersand that made the real feed invalid XML', async () => {
        getBlogposts.mockReturnValue([
            createPost({
                description: 'OWASPAr Cornucopia Website App 2.1 & Mobile App 1.1!',
            }),
        ]);

        const response = await GET();
        const body = await response.text();

        expect(body).toContain('Website App 2.1 &amp; Mobile App 1.1!');
        expect(body).not.toMatch(unescapedAmpersand);
    });
});
