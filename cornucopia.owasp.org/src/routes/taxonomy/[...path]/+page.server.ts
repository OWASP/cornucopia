import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import path from "path";

/** @type {import('./$types').PageServerLoad} */
export async function load({ url }) {
  const lang = 'en';
  let [categories, content] = FileSystemHelper.getDataByRoute(url.pathname, lang);

  // Resolve the canonical path for GitHub links
  let route = url.pathname;
  if (!route.includes(`taxonomy/${lang}`)) route = route.replace(/taxonomy\/?/, `taxonomy/${lang}/`);

  // Resolve actual casing using FileSystemHelper
  // @ts-ignore
  const baseDataPath = path.join(FileSystemHelper.root, "data");
  // @ts-ignore
  const resolvedFullPath = FileSystemHelper.resolveCaseInsensitivePath(baseDataPath, route);
  // @ts-ignore
  const truePath = path.relative(FileSystemHelper.root, resolvedFullPath).replace(/\\/g, '/');

  return {
    categories: categories,
    content: content,
    path: url.pathname,
    truePath: truePath,
    title: FileSystemHelper.getCurrentPageNameByRoute(url.pathname as string),
    timestamp: new Date().toUTCString(),
  };
}
