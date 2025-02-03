import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper.js';

export async function load({params})
{
    return {
        categories : getCategories()
    }
}

function getCategories() : string[]
{
    return FileSystemHelper.getDirectories("./data/taxonomy")
}