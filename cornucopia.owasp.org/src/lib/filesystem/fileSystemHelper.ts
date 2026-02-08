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

  /**
   * Resolves a path in a case-insensitive manner by checking actual directory names.
   * This ensures cross-platform compatibility between case-sensitive and case-insensitive filesystems.
   */
  private static resolveCaseInsensitivePath(basePath: string, relativePath: string): string {
    const parts = relativePath.split('/').filter(p => p.length > 0);
    let currentPath = path.normalize(basePath);
    
    for (const part of parts) {
      if (!fs.existsSync(currentPath)) {
        return path.join(basePath, relativePath); // Path doesn't exist, return as-is
      }
      
      const entries = fs.readdirSync(currentPath, { withFileTypes: true });
      const matchingEntry = entries.find(entry => 
        entry.name.toLowerCase() === part.toLowerCase()
      );
      
      if (matchingEntry) {
        currentPath = path.join(currentPath, matchingEntry.name);
      } else {
        currentPath = path.join(currentPath, part);
      }
    }
    
    return currentPath;
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
    const baseDataPath = FileSystemHelper.root + "data";
    
    if (!route.includes(`taxonomy/${lang}`)) route = route.replace(/taxonomy\/?/, `taxonomy/${lang}/`);
    
    let defaultLangRoute = route.replace(`/taxonomy/${lang}`, '/taxonomy/en');
    
    // Get content using original route structure for Map keys
    let content = FileSystemHelper.getDataFromPath('data' + route).get('data' + route) || "";
    if (content === "") {
      content = FileSystemHelper.getDataFromPath('data' + defaultLangRoute).get('data' + defaultLangRoute) || "";
    }
    
    // Resolve the actual filesystem path for directory operations (case-insensitive)
    const resolvedPath = FileSystemHelper.resolveCaseInsensitivePath(baseDataPath, defaultLangRoute);
    
    if (fs.existsSync(resolvedPath) && fs.lstatSync(resolvedPath).isDirectory()) {
      FileSystemHelper.getDirectories(resolvedPath).forEach(
        (folder) => categories.push(folder));
    }
    
    return [categories, content];
  }

  public static getDataFromPath(filePath: string) : Map<string, string>
  {
    const base = FileSystemHelper.root;
    let content = new Map<string, string>();
  
    // Resolve the actual filesystem path (case-insensitive)
    const resolvedPath = FileSystemHelper.resolveCaseInsensitivePath(base, filePath);
    
    let indexFile: string = path.join(resolvedPath, "index.md");
    if (fs.existsSync(indexFile)) {
      content.set(filePath, fs.readFileSync(indexFile, "utf8"));
    }
  
    let folders: string[];
    try {
      folders = FileSystemHelper.getDirectories(resolvedPath);
    } catch (e) {
      folders = [];
    }
  
    folders.forEach((folder) => {
      const folderIndexFile = path.join(resolvedPath, folder, "index.md");
      if (fs.existsSync(folderIndexFile)) {
        content.set(folder, fs.readFileSync(folderIndexFile, "utf8"));
      }
    });
  
    return content;
  }
}