import type { Author } from '$domain/author/author';

// 1. This is a Type Guard. It proves to TypeScript that the 'unknown' data is actually an 'Author'
function isAuthor(data: unknown): data is Author {
  return typeof data === 'object' && data !== null && 'name' in data;
}

export function parseAuthor(data: unknown): Author {
  // 2. We check the data safely. No 'as Author' assertions needed!
  if (isAuthor(data)) {
    return data; 
  }
  throw new Error('Invalid Author data format');
}

export function getAuthors(): Author[] {
  return [];
}

export function getAuthor(name: string): Author | undefined {
  // 3. Because getAuthors() returns Author[], 'a.name' is naturally typed. No assertions needed.
  return getAuthors().find((a) => a.name === name);
}