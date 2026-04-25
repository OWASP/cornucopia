import { getAuthor } from "../../../domain/author/authorController.js"

import { getBlogpostsByAuthor } from "../../../domain/blogpost/blogpostController.js";

export async function load({params})
{
    return {
        author : getAuthor(params.name),
        blogposts : getBlogpostsByAuthor(params.name)
    }
}
