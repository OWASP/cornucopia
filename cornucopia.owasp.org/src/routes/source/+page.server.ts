import { getPageMetadata } from '$lib/utils/pageMetadata.js';
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";

export async function load(event) {
    const metadata = getPageMetadata(event, 'source', 'https://cornucopia.owasp.org/source');
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/source') };
}