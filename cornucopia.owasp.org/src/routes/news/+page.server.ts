import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper.js'
import { LocalCache } from '$lib/utils/cache.js'
import { getAuthors } from '../../domain/author/authorController.js'
import { getBlogposts } from '../../domain/blogpost/blogpostController.js'
import { PAGINATION } from '$lib/constants'

export async function load (): Promise<Record<string, unknown>> {
  return {
    content: FileSystemHelper.getDataFromPath('data/website/pages/news'),
    posts: await LocalCache(() => getBlogposts(), PAGINATION.PAGE_SIZE, 'posts'),
    authors: await LocalCache(() => getAuthors(), PAGINATION.PAGE_SIZE, 'authors')
  }
}