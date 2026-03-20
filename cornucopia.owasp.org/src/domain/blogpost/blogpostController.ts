import fs from 'node:fs';
import path from 'node:path';
// eslint-disable-next-line @typescript-eslint/ban-ts-comment -- The front-matter library is missing type definitions in this project
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

// Type Guard to safely check front-matter attributes
function isAttributes(attrs: unknown): attrs is Record<string, unknown> {
  return typeof attrs === 'object' && attrs !== null;
}

// Helper to strictly get strings and avoid 'no-base-to-string' errors
function getString(val: unknown): string {
  return typeof val === 'string' ? val : '';
}

export function getBlogposts(): BlogPost[] {
  if (fs.existsSync(BLOG_DIR)) {
    const files = fs.readdirSync(BLOG_DIR);
    
    return files.map((file) => {
      const content = fs.readFileSync(path.join(BLOG_DIR, file), 'utf8');
      
       
      const parsed = fm(content);
      
      // Use destructuring to satisfy prefer-destructuring rule
       
      const { attributes } = parsed;

      // Safely check and assign properties
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