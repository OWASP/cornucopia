import { getPageMetadata } from '$lib/utils/pageMetadata.js';
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";

export async function load(event) {
    const metadata = getPageMetadata(event, 'webshop', 'https://cornucopia.owasp.org/webshop');
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/webshop') };
}