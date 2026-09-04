import { getPageMetadata } from '$lib/utils/pageMetadata.js';
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";

export async function load(_event) {
    const metadata = getPageMetadata('source', 'https://cornucopia.owasp.org/source');
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/source') };
}