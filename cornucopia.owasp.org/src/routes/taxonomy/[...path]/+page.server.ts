import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";


export async function load({ params }) {
  let [files, folders, content, routePath] = FileSystemHelper.getDataByRoute(params.path);
  return {
    files: files,
    folders: folders,
    content: content,
    path: routePath,
    title: FileSystemHelper.getFolderNameByRoute(routePath as string),
    timestamp: new Date().toUTCString(),
  };
}
