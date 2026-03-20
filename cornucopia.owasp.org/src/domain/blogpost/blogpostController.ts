import fs from 'node:fs';
import path from 'node:path';
// eslint-disable-next-line @typescript-eslint/ban-ts-comment -- The front-matter library is missing type definitions
// @ts-ignore - Ignoring missing types for front-matter
import fm from 'front-matter';

const ROOT_DIR = path.resolve(path.dirname(''));
const BLOG_DIR = path.join(ROOT_DIR, 'data/blog');

export interface BlogPost {
  title: string;
  date: string;
  author: string;
  summary: string;
  path: string;
}

function isAttributes(attrs: unknown): attrs is Record<string, unknown> {
  return typeof attrs === 'object' && attrs !== null;
}

function getString(val: unknown): string {
  return typeof val === 'string' ? val : '';
}

export function getBlogposts(): BlogPost[] {
  if (fs.existsSync(BLOG_DIR)) {
    const files = fs.readdirSync(BLOG_DIR);
    
    return files.map((file) => {
      const content = fs.readFileSync(path.join(BLOG_DIR, file), 'utf8');
      const parsed = fm(content);
      const { attributes } = parsed;

      if (isAttributes(attributes)) {
        return {
          title: getString(attributes.title),
          date: getString(attributes.date),
          author: getString(attributes.author),
          summary: getString(attributes.summary),
          path: file.replace('.md', '')
        };
      }
      
      throw new Error(`Invalid frontmatter in ${file}`);
    });
  }
  return [];
}

/**
 * Restored: Returns blogposts filtered by a specific author name.
 * Required for the /author/[name] route.
 */
export function getBlogpostsByAuthor(name: string): BlogPost[] {
  return getBlogposts().filter((post) => post.author === name);
}