 
import { expect, describe, it } from 'vitest';
import { FileSystemHelper } from './fileSystemHelper';
import path from 'node:path';

describe('FileSystemHelper Integration Tests', () => {
  const {root} = FileSystemHelper;

  it('should list directories in the cards path', () => {
    const dirPath = path.join(root, 'data/website/pages/cards');
    const directories = FileSystemHelper.getDirectories(dirPath);
    expect(directories).toBeDefined();
    expect(directories.length).toBeGreaterThan(0);
  });

  it('should verify file existence correctly', () => {
    const filePath = path.join(root, 'data/website/pages/cards/en/index.md');
    expect(FileSystemHelper.hasFile(filePath)).toBe(true);
    expect(FileSystemHelper.hasFile(path.join(root, 'nonexistent.md'))).toBe(false);
  });

  it('should generate a valid ASVSRouteMap', () => {
    const routes = FileSystemHelper.ASVSRouteMap();
    expect(routes).toBeDefined();
    expect(routes.length).toBeGreaterThan(0);
    // Check for a standard path segment
    expect(routes[0].Path).toContain('/taxonomy/ASVS');
  });

  it('should extract current page name from route', () => {
    const route = '/taxonomy/ASVS-4.0.3/architecture/secure-lifecycle';
    const folderName = FileSystemHelper.getCurrentPageNameByRoute(route);
    expect(folderName).toBe('secure-lifecycle');

    expect(FileSystemHelper.getCurrentPageNameByRoute('')).toBe('Requirements Mapping');
  });
});