import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import path from "path";
import type { PageMetadata } from "$lib/types/metadata.js";

/** @type {import('./$types').PageServerLoad} */
export async function load({ url }) {
  const lang = 'en';
  const [categories, content] = FileSystemHelper.getDataByRoute(url.pathname, lang);

  let route = url.pathname;
  if (!route.includes(`taxonomy/${lang}`)) route = route.replace(/taxonomy\/?/, `taxonomy/${lang}/`);

  // @ts-expect-error: type override required
  const baseDataPath = path.join(FileSystemHelper.root, "data");
  // @ts-expect-error: type override required
  const resolvedFullPath = FileSystemHelper.resolveCaseInsensitivePath(baseDataPath, route);
  // @ts-expect-error: type override required
  const truePath = path.relative(FileSystemHelper.root, resolvedFullPath).replace(/\\/g, '/');

  const pageTitle = FileSystemHelper.getCurrentPageNameByRoute(url.pathname as string);

  const metadata: PageMetadata = {
      title: `${pageTitle} | OWASP Cornucopia Taxonomy`,
      description: pageTitle,
      keywords: 'OWASP, Cornucopia, taxonomy, threat modeling, requirements',
      canonicalUrl: `https://cornucopia.owasp.org${encodeURI(url.pathname)}`,
      type: 'website',
  };

  return {
    metadata,
    categories,
    content,
    path: url.pathname,
    truePath,
    title: pageTitle,
    timestamp: new Date().toUTCString(),
  };
}