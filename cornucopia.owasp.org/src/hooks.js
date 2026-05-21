/** @type {import('@sveltejs/kit').Reroute} */
export function reroute({ url }) {
  const pathMatch = url.pathname.match(/^\/(en|uk)(?=\/|$)/i);
  if (!pathMatch) {
    return;
  }

  const strippedPath = url.pathname.replace(/^\/(en|uk)(?=\/|$)/i, '') || '/';

  if (
    strippedPath.startsWith('/_app') ||
    strippedPath.startsWith('/api') ||
    strippedPath.startsWith('/build') ||
    strippedPath === '/favicon.ico' ||
    strippedPath === '/robots.txt' ||
    strippedPath === '/rss.xml' ||
    strippedPath === '/sitemap.xml'
  ) {
    return;
  }

  return strippedPath;
}

/** @type {import('@sveltejs/kit').Transport} */
export const transport = {};
