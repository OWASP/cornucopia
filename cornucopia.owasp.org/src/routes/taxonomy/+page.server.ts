import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper.js';
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load(event)
{
    const t = event.locals.translation;
    const fb = event.locals.fallbackTranslation;
    const metadata: PageMetadata = {
        title: t?.taxonomy?.head?.title ?? fb?.taxonomy?.head?.title ?? 'OWASP Cornucopia - Requirements & Cross-references',
        description: t?.taxonomy?.head?.description ?? fb?.taxonomy?.head?.description ?? '',
        keywords: t?.taxonomy?.head?.keywords ?? fb?.taxonomy?.head?.keywords ?? '',
        canonicalUrl: 'https://cornucopia.owasp.org/taxonomy',
        type: 'website',
    };
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