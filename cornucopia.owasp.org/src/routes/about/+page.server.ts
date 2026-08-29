import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load({ params: _params }) {
    const metadata: PageMetadata = {
        title: 'About | OWASP Cornucopia',
        description: 'Learn about OWASP Cornucopia, the card game that helps software development teams identify security requirements.',
        keywords: 'OWASP, Cornucopia, about, security, card game',
        canonicalUrl: 'https://cornucopia.owasp.org/about',
        type: 'website',
    };
    const content = FileSystemHelper.getDataFromPath('data/website/pages/about');
    return { metadata, content };
}