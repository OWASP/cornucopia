import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load({ params: _params }) {
    const metadata: PageMetadata = {
        title: 'Webshop | OWASP Cornucopia',
        description: 'Purchase official OWASP Cornucopia card decks and printed editions.',
        keywords: 'OWASP, Cornucopia, webshop, buy, card deck',
        canonicalUrl: 'https://cornucopia.owasp.org/webshop',
        type: 'website',
    };
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/webshop') };
}