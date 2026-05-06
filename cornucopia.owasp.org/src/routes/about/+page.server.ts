import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";


export async function load({ params: _params }) {
    const content = FileSystemHelper.getDataFromPath('data/website/pages/about');
    return {
        content: content
    };
}