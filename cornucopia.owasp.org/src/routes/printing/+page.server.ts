import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";

export async function load({ params: _params }) {
    return {
        content: FileSystemHelper.getDataFromPath('data/website/pages/printing')
    };
}