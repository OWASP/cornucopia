import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load({ params: _params }) {
    const metadata: PageMetadata = {
        title: 'Tribute | OWASP Cornucopia',
        description: 'Tribute to the contributors and supporters of OWASP Cornucopia.',
        keywords: 'OWASP, Cornucopia, tribute, contributors',
        canonicalUrl: 'https://cornucopia.owasp.org/tribute',
        type: 'website',
    };
    const content = FileSystemHelper.getDataFromPath('data/website/pages/tribute');
    return { metadata, content };
}