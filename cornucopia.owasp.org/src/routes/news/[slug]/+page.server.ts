import { LocalCache } from "$lib/utils/cache.js";
import { getBlogpostByTitle } from "../../../domain/blogpost/blogpostController.js";
export async function load({params})
{
    const title : string = params.slug.toLowerCase();
    const blogpost = await LocalCache(()=>getBlogpostByTitle(title),20,title);
    return {
        blogpost,
        title: blogpost.title ? blogpost.title + " | OWASP Cornucopia" : null,
        description: blogpost.description || null,
        url: "https://cornucopia.owasp.org/news/" + blogpost.path,
        ogType: "article"
    }
}