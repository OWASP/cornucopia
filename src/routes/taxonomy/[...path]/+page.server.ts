import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import fs from "fs";

export async function load({ params }) {
  let filePath: string = "./data/taxonomy/" + params.path;
  let [files, folders, content] = getDataFromPath(filePath);

  return {
    files: files,
    folders: folders,
    content: content,
    path: params.path,
    timestamp: new Date().toUTCString(),
  };
  /*
    return {
        category : params.category,
        entry : params.entry,
        markdown : getMarkdown(params.category, params.entry)
    }
    */
}

function getDataFromPath(path: string) {
  let resultFolders = [];
  let resultFiles = [];

  let content: string = "";
  let indexFile: string = path + "/index.md";
  if (fs.existsSync(indexFile)) content = fs.readFileSync(indexFile, "utf8");
  else {
    //console.log('🍎 ' + indexFile + ' doesnt exist')
  }
  var parentdir = path.split("/").slice(0, -1).join("/");
  let disclaimerFile: string = parentdir + "/Disclaimer.md";
  if (fs.existsSync(disclaimerFile)) {
    content += "\r\n" +fs.readFileSync(disclaimerFile, "utf8");
  }

  let folders = FileSystemHelper.getDirectories(path);

  for (let i = 0; i < folders.length; i++) {
    let folderName = folders[i];
    let folder = path + "/" + folderName;
    let files = FileSystemHelper.getFiles(folder);
    files.includes("index.md")
      ? resultFolders.push(folderName)
      : resultFiles.push(folderName);
  }

  return [resultFiles, resultFolders, content];
}
