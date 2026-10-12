import { getPageMetadata } from '$lib/utils/pageMetadata.js';
import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper.js';

export async function load(_event)
{
    const metadata = getPageMetadata('taxonomy', 'https://cornucopia.owasp.org/taxonomy');
    return {
        metadata,
        content: FileSystemHelper.getDataFromPath('data/website/pages/taxonomy'),
        categories: getCategories()
    };
}

function getCategories(): string[]
{
    return FileSystemHelper.getDirectories("./data/taxonomy/en");
}