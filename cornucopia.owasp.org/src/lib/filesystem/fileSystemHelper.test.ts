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
    
    // Fix: the real code throws an ENOENT error, so we test that it throws!
    expect(() => FileSystemHelper.getDirectories(path.join(root, 'nonexistent'))).toThrow();
  });

  it('should verify file and directory existence correctly', () => {
    const filePath = path.join(root, 'package.json');
    expect(FileSystemHelper.hasFile(filePath)).toBe(true);
    expect(FileSystemHelper.hasFile(path.join(root, 'fake.md'))).toBe(false);
  });

  it('should extract current page name from route correctly', () => {
    const route = '/taxonomy/ASVS-4.0.3/architecture/secure-lifecycle';
    expect(FileSystemHelper.getCurrentPageNameByRoute(route)).toBe('secure-lifecycle');
    expect(FileSystemHelper.getCurrentPageNameByRoute('')).toBe('Requirements Mapping');
  });
});