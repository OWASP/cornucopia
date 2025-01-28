import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";

export async function load({ params }) {
    return {
        content: FileSystemHelper.getDataFromPath('data/website/pages/questionsandanswers')
    };
}