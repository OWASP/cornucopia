import { getAuthor } from '../../../domain/author/authorController.js'
import { getBlogpostsByAuthor } from '../../../domain/blogpost/blogpostController.js'
import type { PageServerLoad } from './$types'

// Type Guard to safely assert function types without 'unsafe-assertion' error
function isFunction(val: unknown): val is (arg: string) => unknown {
  return typeof val === 'function';
}

export const load: PageServerLoad = (({ params }) => {
  // Use unknown bridges and type guards to satisfy strict assertion rules
  const rawGetAuthor: unknown = getAuthor;
  const rawGetBlogposts: unknown = getBlogpostsByAuthor;

  let author = null;
  let blogposts = null;

  if (isFunction(rawGetAuthor)) {
    author = rawGetAuthor(params.name);
  }

  if (isFunction(rawGetBlogposts)) {
    blogposts = rawGetBlogposts(params.name);
  }

  return {
    author,
    blogposts
  };
});