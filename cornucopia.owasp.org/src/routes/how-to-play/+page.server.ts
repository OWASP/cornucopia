import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper.js';
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load({ params: _params })
{
    const metadata: PageMetadata = {
        title: 'How to Play | OWASP Cornucopia',
        description: 'Learn how to play OWASP Cornucopia and use it in your security requirements process.',
        keywords: 'OWASP, Cornucopia, how to play, instructions, guide',
        canonicalUrl: 'https://cornucopia.owasp.org/how-to-play',
        type: 'website',
    };
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/play') };
}