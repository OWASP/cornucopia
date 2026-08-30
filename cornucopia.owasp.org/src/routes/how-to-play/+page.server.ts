import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper.js';
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load(event)
{
    const t = event.locals.translation;
    const fb = event.locals.fallbackTranslation;
    const metadata: PageMetadata = {
        title: t?.play?.head?.title ?? fb?.play?.head?.title ?? 'OWASP Cornucopia - How to play',
        description: t?.play?.head?.description ?? fb?.play?.head?.description ?? '',
        keywords: t?.play?.head?.keywords ?? fb?.play?.head?.keywords ?? '',
        canonicalUrl: 'https://cornucopia.owasp.org/how-to-play',
        type: 'website',
    };
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/play') };
}