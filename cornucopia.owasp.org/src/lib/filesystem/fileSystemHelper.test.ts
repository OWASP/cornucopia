/* eslint-disable @typescript-eslint/no-magic-numbers -- Bypassing for test assertions */
import { expect, describe, it } from 'vitest';
import { FileSystemHelper } from './fileSystemHelper';
import path from 'node:path';

describe('FileSystemHelper Integration & Coverage Tests', () => {
  const { root } = FileSystemHelper;

  it('should list directories and handle non-existent ones', () => {
    const dirPath = path.join(root, 'src');
    const directories = FileSystemHelper.getDirectories(dirPath);
    expect(directories).toBeDefined();
    expect(Array.isArray(directories)).toBe(true);

    // Coverage: Test a path that doesn't exist to hit the error/empty branch
    const fakePath = path.join(root, 'nonexistent_folder_xyz');
    expect(FileSystemHelper.getDirectories(fakePath)).toEqual([]);
  });

  it('should verify file and directory existence correctly', () => {
    const filePath = path.join(root, 'package.json');
    expect(FileSystemHelper.hasFile(filePath)).toBe(true);
    expect(FileSystemHelper.hasFile(path.join(root, 'ghost_file.md'))).toBe(false);
    
    expect(FileSystemHelper.hasDir(path.join(root, 'src'))).toBe(true);
    expect(FileSystemHelper.hasDir(path.join(root, 'fake_src_dir'))).toBe(false);
  });

  it('should extract current page name from route correctly', () => {
    const route = '/taxonomy/ASVS-4.0.3/architecture/secure-lifecycle';
    expect(FileSystemHelper.getCurrentPageNameByRoute(route)).toBe('secure-lifecycle');

    // Hits the 'Requirements Mapping' default branch
    expect(FileSystemHelper.getCurrentPageNameByRoute('')).toBe('Requirements Mapping');
    expect(FileSystemHelper.getCurrentPageNameByRoute('/')).toBe('Requirements Mapping');
  });

  it('should generate a valid ASVSRouteMap', () => {
    const routes = FileSystemHelper.ASVSRouteMap();
    expect(routes).toBeDefined();
    if (routes.length > 0) {
      expect(routes[0].Path).toBeDefined();
    }
  });
});