import { getBlogposts } from '$domain/blogpost/blogpostController'
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = ({ params }) => {
  const posts = getBlogposts()
  const post = posts.find((p) => p.path === params.slug)
  if (post === undefined) {
    throw new Error(`Post not found: ${params.slug}`)
  }
  return { post }
}