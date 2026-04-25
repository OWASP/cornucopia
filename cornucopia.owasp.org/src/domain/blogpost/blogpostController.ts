import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import fs from 'fs'
import fm from "front-matter"
import type { Blogpost } from "./blogpost";
import { LocalCacheSync } from "$lib/utils/cache";

export function getBlogposts() : Blogpost[]
{
    const result : Blogpost[] = []
    const basepath : string = "./data/news";

    // Collect all directories
    const directories = FileSystemHelper.getDirectories(basepath);

    // For every directory, fetch the 'index.md' file
    for(let i = 0 ; i < directories.length ; i++)
    {
        const directory = directories[i].toLowerCase();
        const filepath = basepath + '/' + directory + '/index.md'
        const file = fs.readFileSync(filepath, 'utf8');
        const parsed = fm(file);
        const post : Blogpost = 
        {
            title : directory.substring(9),
            markdown : parsed.body,
            // @ts-expect-error: type override required
            author : parsed.attributes.author,
            // @ts-expect-error: type override required
            hidden : parsed.attributes.hidden,
            // @ts-expect-error: type override required
            date : parsed.attributes.date,
            // @ts-expect-error: type override required
            tags : parsed.attributes.tags.split(','),
            // @ts-expect-error: type override required
            path : directory,
            // @ts-expect-error: type override required
            description : parsed.attributes.description
        }
        // check if the post is hidden
        if(post.hidden)
        {
            console.log("🔴 Skipping blogpost because set to hidden: [" + directory + "]")
            continue;
        }

        // Check the post date
        const today = new Date();
        const year = today.getFullYear();
        const month = ('' + (today.getMonth() + 1)).padStart(2,'0')
        const day = ('' + (today.getDate())).padStart(2,'0')
        const todayAsString = year + month + day;
        const compare = (post.date + '').localeCompare(todayAsString);
        if( compare > 0)
        {
            console.log("🔴 Skipping blogpost because release date is " + post.date + " and today is " + todayAsString +   ": [" + post.title + "]")
            continue;
        }

        console.log("🟢 Added blogpost: [" + post.title + "]")
        result.push(post)
    }

    result.sort((a : Blogpost, b : Blogpost) => ('' + b.date).localeCompare(a.date))
    return result;
}

export function getBlogpostsByAuthor(name : string) : Blogpost[]
{
    const blogposts : Blogpost[] = LocalCacheSync(getBlogposts,20,'posts');
    return blogposts.filter(post => post.author == name);
}

export function getBlogpostByTitle(title : string) : Blogpost
{
    const blogposts : Blogpost[] = LocalCacheSync(getBlogposts,20,'posts');
    return blogposts.find(post => {return post.path == title}) || {} as Blogpost
}