import { getPageMetadata } from '$lib/utils/pageMetadata.js';
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";

export async function load(_event) {
    const metadata = getPageMetadata('printing', 'https://cornucopia.owasp.org/printing');
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/printing') };
}