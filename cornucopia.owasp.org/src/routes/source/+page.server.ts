import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load(event) {
    const t = event.locals.translation;
    const fb = event.locals.fallbackTranslation;
    const metadata: PageMetadata = {
        title: t?.source?.head?.title ?? fb?.source?.head?.title ?? 'OWASP Cornucopia - Source Code',
        description: t?.source?.head?.description ?? fb?.source?.head?.description ?? '',
        keywords: t?.source?.head?.keywords ?? fb?.source?.head?.keywords ?? '',
        canonicalUrl: 'https://cornucopia.owasp.org/source',
        type: 'website',
    };
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/source') };
}