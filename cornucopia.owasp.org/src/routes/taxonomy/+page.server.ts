import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper.js';
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load({ params: _params })
{
    const metadata: PageMetadata = {
        title: 'Taxonomy | OWASP Cornucopia',
        description: 'Browse the OWASP Cornucopia taxonomy of security requirements and threat categories.',
        keywords: 'OWASP, Cornucopia, taxonomy, threat modeling, requirements',
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