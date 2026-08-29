import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load({ params: _params }) {
    const metadata: PageMetadata = {
        title: 'Source | OWASP Cornucopia',
        description: 'Access the source files and raw data behind OWASP Cornucopia.',
        keywords: 'OWASP, Cornucopia, source, data, files',
        canonicalUrl: 'https://cornucopia.owasp.org/source',
        type: 'website',
    };
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/source') };
}