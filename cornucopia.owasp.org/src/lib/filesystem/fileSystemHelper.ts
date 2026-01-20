import fs from "fs";
import type { Route } from "../../domain/routes/route";
import path from 'path';
import { fileURLToPath } from 'url';

export class FileSystemHelper {

  //private static root = path.normalize(path.dirname(fileURLToPath(import.meta.url)) + '/../../../');


  private static root = (() => {
    // During development and build, calculate root from import.meta.url

    if (import.meta.url.includes('.svelte-kit')) {
      return path.normalize(path.dirname(fileURLToPath(import.meta.url)) + '/../../../../');
    }

    return path.normalize(path.dirname(fileURLToPath(import.meta.url)) + '/../../../');

  })();

  public static hasDir(path: string): boolean {
    return fs.existsSync(path);
  }

  public static hasFile(path: string): boolean {
    return FileSystemHelper.hasDir(path) && fs.lstatSync(path).isFile();
  }

  public static getDirectories(path: string): string[] {
    return fs
      .readdirSync(path, { withFileTypes: true })
      .filter((x) => x.isDirectory())
      .map((dirent) => dirent.name);
  }

  public static getFiles(path: string): string[] {
    return fs
      .readdirSync(path, { withFileTypes: true })
      .filter((x) => x.isFile())
      .map((dirent) => dirent.name);
  }

  public static ASVSRouteMap(version: string = "4.0.3"): Route[] {
    const basePath: string = `data/taxonomy/en/ASVS-${version}`;
    const sectionRegex = /^(\d{2})-/;
    let routes: Route[] = [];

    const firstLevelDirs = this.getDirectories(FileSystemHelper.root + basePath).filter((dir) =>
      sectionRegex.test(dir)
    );

    firstLevelDirs.forEach((firstLevelDir) => {
      const firstLevelPath = basePath + '/' + firstLevelDir;
      const firstPart = firstLevelDir.match(sectionRegex)?.[1];

      const secondLevelDirs = this.getDirectories(FileSystemHelper.root + firstLevelPath).filter(
        (dir) => sectionRegex.test(dir)
      );

      secondLevelDirs.forEach((secondLevelDir) => {
        const secondPart = secondLevelDir.match(sectionRegex)?.[1];
        const section = `${firstPart}.${secondPart}`;
        let fullPath = firstLevelPath + '/' + secondLevelDir;
        fullPath = fullPath.replace("data/taxonomy/en", "/taxonomy");

        routes.push({
          Path: fullPath,
          Section: section,
        });
      });
    });

    return routes;
  }

  public static getCurrentPageNameByRoute(route: string) {
    return route ? route.split('/').slice(-1)[0] : 'Requirements Mapping';
  }

  public static getDataByRoute(route: string, lang: string = 'en'): [string[], string] {
    let categories: string[] = [];
    let filePath : string = FileSystemHelper.root + "data";
    if (!route.includes(`taxonomy/${lang}`)) route = route.replace(/taxonomy\/?/, `taxonomy/${lang}/`);
    
    let defaultLangRoute = route.replace(`/taxonomy/${lang}`, '/taxonomy/en', );
    let content = FileSystemHelper.getDataFromPath('data' + route).get('data' + route) || "";
    if (content === "") {
      content = FileSystemHelper.getDataFromPath('data' + defaultLangRoute).get('data' + defaultLangRoute) || "";
    }
    FileSystemHelper.getDirectories(path.normalize(filePath + defaultLangRoute)).forEach(
      (folder) => categories.push(folder));
    
    return [categories, content];
  }

  public static getDataFromPath(filePath: string) : Map<string, string>
  {
    const base = FileSystemHelper.root + "/";
    let content = new Map<string, string>();
  
    let indexFile: string = path.normalize(base + filePath + "/index.md");
    if (fs.existsSync(indexFile)) {
      content.set(filePath, fs.readFileSync(indexFile, "utf8"));
    }
  
    let folders: string[];
    try {
      folders = FileSystemHelper.getDirectories(path.normalize(base + filePath));
    } catch (e) {
      folders = [];
    }
    if (folders.length == 0) console.log("No folders found for path: " + path.normalize(base + filePath));
  
    folders.forEach((folder) => {
      if (fs.existsSync(path.normalize(base + filePath + "/" + folder + "/index.md"))) {
        content.set(folder, fs.readFileSync(path.normalize(base + filePath + "/" + folder + "/index.md"), "utf8"));
      }
    });
  
    return content;
  }
}