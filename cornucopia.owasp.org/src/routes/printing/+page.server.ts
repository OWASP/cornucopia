import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load({ params: _params }) {
    const metadata: PageMetadata = {
        title: 'Printing | OWASP Cornucopia',
        description: 'Instructions and resources for printing your own OWASP Cornucopia card deck.',
        keywords: 'OWASP, Cornucopia, printing, print, card deck',
        canonicalUrl: 'https://cornucopia.owasp.org/printing',
        type: 'website',
    };
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/printing') };
}