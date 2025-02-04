import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import type { Author } from "./author";
import fm from "front-matter";
import fs from "fs";

export function getAuthor(name: string): Author {
  return getAuthors().find((x) => x.name == name) || ({} as Author);
}

export function getAuthors(): Author[] {
  let authors: Author[] = new Array<Author>();
  let dirs = FileSystemHelper.getDirectories("./data/author");

  for (let i = 0; i < dirs.length; i++) {
    let dir = dirs[i];
    let filepath = "./data/author/" + dir + "/index.md";
    let file = fs.readFileSync(filepath, "utf8");
    let parsed: any = fm(file);

    let author: Author = {} as Author;
    author.name = dir;
    author.website = parsed?.attributes?.website ?? "";
    author.linkedin = parsed?.attributes?.linkedin ?? "";
    author.email = parsed?.attributes?.email ?? "";
    author.bio = parsed.body;

    // Skip default author
    if (author.name == "undefined") continue;

    authors.push(author);
  }

  return authors;
}
