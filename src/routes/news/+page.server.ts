import { LocalCache } from '$lib/utils/cache.js'
import { getAuthors } from '../../domain/author/authorController.js'
import { getBlogposts } from '../../domain/blogpost/blogpostController.js'

export async function load({params})
{
    return {
        posts : await LocalCache(()=>getBlogposts(),20,'posts'),
        authors : await LocalCache(()=>getAuthors(),20,'authors'),
    }
}


