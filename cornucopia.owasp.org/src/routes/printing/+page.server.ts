import { getPageMetadata } from '$lib/utils/pageMetadata.js';
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";

export async function load(event) {
    const metadata = getPageMetadata(event, 'printing', 'https://cornucopia.owasp.org/printing');
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/printing') };
}