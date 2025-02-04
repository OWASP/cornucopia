import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";


export async function load({ params }) {
    let content = FileSystemHelper.getDataFromPath('data/website/pages/about');
    return {
        content: content
    };
}