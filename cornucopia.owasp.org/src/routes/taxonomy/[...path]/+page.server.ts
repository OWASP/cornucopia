import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";


export async function load({ params, url }) {
  let [categories, content] = FileSystemHelper.getDataByRoute(url.pathname, 'en');
  return {
    categories: categories,
    content: content,
    path: url.pathname,
    title: FileSystemHelper.getCurrentPageNameByRoute(url.pathname as string),
    timestamp: new Date().toUTCString(),
  };
}
