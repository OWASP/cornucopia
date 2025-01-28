import { LocalCache } from "$lib/utils/cache.js";
import { getBlogpostByTitle } from "../../../domain/blogpost/blogpostController.js";

export async function load({params})
{
    let title : string = params.slug.toLowerCase();
    return {
        blogpost : await LocalCache(()=>getBlogpostByTitle(title),20,title)
    }
}