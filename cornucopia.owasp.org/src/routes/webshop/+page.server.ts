import { getPageMetadata } from '$lib/utils/pageMetadata.js';
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";

export async function load(_event) {
    const metadata = getPageMetadata('webshop', 'https://cornucopia.owasp.org/webshop');
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/webshop') };
}