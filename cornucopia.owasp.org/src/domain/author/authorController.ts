import type { Author } from '$domain/author/author';

function isAuthor(data: unknown): data is Author {
  return typeof data === 'object' && data !== null && 'name' in data;
}

export function parseAuthor(data: unknown): Author {
  if (isAuthor(data)) {
    return data;
  }
  throw new Error('Invalid Author data format');
}

export function getAuthors(): Author[] {
  return [];
}

export function getAuthor(name: string): Author | undefined {
  return getAuthors().find((a) => a.name === name);
}