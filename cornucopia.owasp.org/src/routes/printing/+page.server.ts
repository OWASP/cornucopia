import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load(event) {
    const t = event.locals.translation;
    const fb = event.locals.fallbackTranslation;
    const metadata: PageMetadata = {
        title: t?.printing?.head?.title ?? fb?.printing?.head?.title ?? 'OWASP Cornucopia - Printing Guidelines',
        description: t?.printing?.head?.description ?? fb?.printing?.head?.description ?? '',
        keywords: t?.printing?.head?.keywords ?? fb?.printing?.head?.keywords ?? '',
        canonicalUrl: 'https://cornucopia.owasp.org/printing',
        type: 'website',
    };
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/printing') };
}