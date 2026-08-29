import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load({ params: _params }) {
    const metadata: PageMetadata = {
        title: 'Roadmap | OWASP Cornucopia',
        description: 'The development roadmap and future plans for OWASP Cornucopia.',
        keywords: 'OWASP, Cornucopia, roadmap, plans, development',
        canonicalUrl: 'https://cornucopia.owasp.org/roadmap',
        type: 'website',
    };
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/roadmap') };
}