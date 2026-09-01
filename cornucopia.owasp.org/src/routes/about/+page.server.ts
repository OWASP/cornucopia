import { getPageMetadata } from '$lib/utils/pageMetadata.js';
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";

export async function load(event) {
    const metadata = getPageMetadata(event, 'about', 'https://cornucopia.owasp.org/about');
    const content = FileSystemHelper.getDataFromPath('data/website/pages/about');
    return { metadata, content };
}