import { getPageMetadata } from '$lib/utils/pageMetadata.js';
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";

export async function load(_event) {
    const metadata = getPageMetadata('copi', 'https://cornucopia.owasp.org/copi');
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/copi') };
}