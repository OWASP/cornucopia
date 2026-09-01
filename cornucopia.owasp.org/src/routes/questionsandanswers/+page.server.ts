import { getPageMetadata } from '$lib/utils/pageMetadata.js';
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";

export async function load(event) {
    const metadata = getPageMetadata(event, 'questionsandanswers', 'https://cornucopia.owasp.org/questionsandanswers');
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/questionsandanswers') };
}