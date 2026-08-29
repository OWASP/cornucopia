import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load({ params: _params }) {
    const metadata: PageMetadata = {
        title: 'Swag | OWASP Cornucopia',
        description: 'OWASP Cornucopia merchandise and swag.',
        keywords: 'OWASP, Cornucopia, swag, merchandise',
        canonicalUrl: 'https://cornucopia.owasp.org/swags',
        type: 'website',
    };
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/swags') };
}