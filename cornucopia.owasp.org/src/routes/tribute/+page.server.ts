import { getPageMetadata } from '$lib/utils/pageMetadata.js';
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";

export async function load(event) {
    const metadata = getPageMetadata(event, 'tribute', 'https://cornucopia.owasp.org/tribute');
    const content = FileSystemHelper.getDataFromPath('data/website/pages/tribute');
    return { metadata, content };
}