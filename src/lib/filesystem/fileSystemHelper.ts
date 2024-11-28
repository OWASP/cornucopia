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
    const basePath: string = "data/taxonomy-en/ASVS-4.0.3";
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
        fullPath = fullPath.replace("data/taxonomy-en", "/taxonomy");

        routes.push({
          Path: fullPath,
          Section: section,
        });
      });
    });

    return routes;
  }

  public static MASVSRouteMap(): Route[] {
    const basePath: string = "data/taxonomy-en/masvs-2.1.0";
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
        fullPath = fullPath.replace("data/taxonomy-en", "/taxonomy");

        routes.push({
          Path: fullPath,
          Section: section,
        });
      });
    });

    return routes;
  }

  public static MASTGRouteMap(): Route[] {
    const basePath: string = "data/taxonomy-en/mastg-1.7.0";
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
        fullPath = fullPath.replace("data/taxonomy-en", "/taxonomy");

        routes.push({
          Path: fullPath,
          Section: section,
        });
      });
    });

    return routes;
  }
}
