import fs from "fs";
import type { Route } from "../../domain/routes/route";

export class FileSystemHelper {

  public static hasDir(path: string): boolean {
    return fs.existsSync(path);
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

  public static ASVSRouteMap(): Route[] {
    const basePath: string = "data/taxonomy/en/ASVS-4.0.3";
    const sectionRegex = /^(\d{2})-/;
    let routes: Route[] = [];

    const firstLevelDirs = this.getDirectories(basePath).filter((dir) =>
      sectionRegex.test(dir)
    );

    firstLevelDirs.forEach((firstLevelDir) => {
      const firstLevelPath = basePath + '/' + firstLevelDir;
      const firstPart = firstLevelDir.match(sectionRegex)?.[1];

      const secondLevelDirs = this.getDirectories(firstLevelPath).filter(
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

  public static getFolderNameByRoute(route: string) {
    let base: string = "data/taxonomy/en";
    let path: string = base;
    let routes: string[] = route.split('/');

    routes.forEach((dir) => {
      let dirs = this.getDirectories(path);
      dirs.forEach((folder) => {
        if (dir != folder.toLowerCase()) return;
        path = path + '/' + folder;
      });
    });

    if (path == base) return 'Requirements Mapping';

    return path.split('/').slice(-1);
  }

  public static getDataByRoute(route: string) {
    let resultFolders: string[] = [];
    let resultFiles: string[] = [];
    let routePath: string = '';
    let path : string = "data/taxonomy/en";
    let routes: string[] = route.split('/');

    routes.forEach((dir) => {
      let dirs = this.getDirectories(path);
      dirs.forEach((folder) => {
        if (dir != folder.toLowerCase()) return;
        path = path + '/' + folder;
      });
    });
    routePath = path.toLowerCase().replace('data/taxonomy/en/', '');

    let content: string = "";
    let indexFile: string = path + "/index.md";
    if (fs.existsSync(indexFile)) content = fs.readFileSync(indexFile, "utf8");
    let folders = FileSystemHelper.getDirectories(path);

    folders.forEach((folder) => {
      let files = FileSystemHelper.getFiles(path + "/" + folder);
      files.includes("index.md")
        ? resultFolders.push(folder)
        : resultFiles.push(folder);
    });
  
    return [resultFiles, resultFolders, content, routePath];
  }

  public static getDataFromPath(path: string) : Map<string, string>
  {
    let content = new Map<string, string>;
  
    let indexFile: string = path + "/index.md";
    if (fs.existsSync(indexFile)) {
      content.set(path, fs.readFileSync(indexFile, "utf8"));
    }
  
    let folders: string[];
    try {
      folders = FileSystemHelper.getDirectories(path);
    } catch (e) {
      folders = [];
    }
    if (folders.length == 0) console.log("No folders found for path: " + path);
  
    folders.forEach((folder) => {
      if (fs.existsSync(path + "/" + folder + "/index.md")) {
        content.set(folder, fs.readFileSync(path + "/" + folder + "/index.md", "utf8"));
      }
    });
  
    return content;
  }
}