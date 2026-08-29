import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load({ params: _params }) {
    const metadata: PageMetadata = {
        title: 'Copi | OWASP Cornucopia',
        description: 'Play OWASP Cornucopia online with Copi, the digital companion for the card game.',
        keywords: 'OWASP, Cornucopia, Copi, online, play',
        canonicalUrl: 'https://cornucopia.owasp.org/copi',
        type: 'website',
    };
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/copi') };
}