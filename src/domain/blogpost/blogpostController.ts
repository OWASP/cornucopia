import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import fs from 'fs'
import fm from "front-matter"
import type { Blogpost } from "./blogpost";
import { LocalCacheSync } from "$lib/utils/cache";

export function getBlogposts() : Blogpost[]
{
    let result : Blogpost[] = []
    let basepath : string = "./data/news";

    // Collect all directories
    let directories = FileSystemHelper.getDirectories(basepath);

    // For every directory, fetch the 'index.md' file
    for(let i = 0 ; i < directories.length ; i++)
    {
        let directory = directories[i].toLowerCase();
        let filepath = basepath + '/' + directory + '/index.md'
        let file = fs.readFileSync(filepath, 'utf8');
        let parsed = fm(file);
        let post : Blogpost = 
        {
            title : directory.substring(9),
            markdown : parsed.body,
            //@ts-ignore
            author : parsed.attributes.author,
            //@ts-ignore
            hidden : parsed.attributes.hidden,
            //@ts-ignore
            date : parsed.attributes.date,
            //@ts-ignore
            tags : parsed.attributes.tags.split(','),
            //@ts-ignore
            path : directory,
            //@ts-ignore
            description : parsed.attributes.description
        }
        // check if the post is hidden
        if(post.hidden)
        {
            console.log("🔴 Skipping blogpost because set to hidden: [" + directory + "]")
            continue;
        }

        // Check the post date
        let today = new Date();
        let year = today.getFullYear();
        let month = ('' + (today.getMonth() + 1)).padStart(2,'0')
        let day = ('' + (today.getDate())).padStart(2,'0')
        let todayAsString = year + month + day;
        let compare = (post.date + '').localeCompare(todayAsString);
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
    let blogposts : Blogpost[] = LocalCacheSync(getBlogposts,20,'posts');
    return blogposts.filter(post => post.author == name);
}

export function getBlogpostByTitle(title : string) : Blogpost
{
    let blogposts : Blogpost[] = LocalCacheSync(getBlogposts,20,'posts');
    return blogposts.find(post => {return post.path == title}) || {} as Blogpost
}