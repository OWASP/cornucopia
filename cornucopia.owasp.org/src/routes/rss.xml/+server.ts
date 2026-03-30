import { getBlogposts } from '$domain/blogpost/blogpostController';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = () => {
  const posts = getBlogposts();
  const siteUrl = 'https://cornucopia.owasp.org';

  const xml = `<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0" xmlns:atom="http://www.w3.org/2000/xml/atom">
    <channel>
      <title>OWASP Cornucopia Blog</title>
      <link>${siteUrl}</link>
      <description>Threat Modeling with OWASP Cornucopia</description>
      <atom:link href="${siteUrl}/rss.xml" rel="self" type="application/rss+xml" />
      ${posts
        .map(
          (post) => `
            <item>
              <title>${post.title}</title>
              <link>${siteUrl}/news/${post.path}</link>
              <description>${post.description}</description>
              <pubDate>${new Date(post.date).toUTCString()}</pubDate>
              <guid>${siteUrl}/news/${post.path}</guid>
            </item>
          `
        )
        .join('')}
    </channel>
    </rss>`;

  return new Response(xml, {
    headers: {
      'Cache-Control': 'max-age=0, s-maxage=3600',
      'Content-Type': 'application/xml'
    }
  });
};