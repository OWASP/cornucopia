import { getPageMetadata } from '$lib/utils/pageMetadata.js';
import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper.js';

export async function load(_event)
{
    const metadata = getPageMetadata('play', 'https://cornucopia.owasp.org/how-to-play');
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/play') };
}