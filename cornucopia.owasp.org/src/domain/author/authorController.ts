import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import type { Author } from "./author";
import fm from "front-matter";
import fs from "fs";

export function getAuthor(name: string): Author {
  return getAuthors().find((x) => x.name == name) || ({} as Author);
}

export function getAuthors(): Author[] {
  const authors: Author[] = new Array<Author>();
  const dirs = FileSystemHelper.getDirectories("./data/author");

  for (let i = 0; i < dirs.length; i++) {
    const dir = dirs[i];
    const filepath = "./data/author/" + dir + "/index.md";
    const file = fs.readFileSync(filepath, "utf8");
    const parsed = fm<{ website: string; linkedin: string; email: string }>(file);

    const author: Author = {} as Author;
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
