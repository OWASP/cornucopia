import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load(event) {
    const t = event.locals.translation;
    const fb = event.locals.fallbackTranslation;
    const metadata: PageMetadata = {
        title: t?.tribute?.head?.title ?? fb?.tribute?.head?.title ?? 'OWASP Cornucopia - Tribute',
        description: t?.tribute?.head?.description ?? fb?.tribute?.head?.description ?? '',
        keywords: t?.tribute?.head?.keywords ?? fb?.tribute?.head?.keywords ?? '',
        canonicalUrl: 'https://cornucopia.owasp.org/tribute',
        type: 'website',
    };
    const content = FileSystemHelper.getDataFromPath('data/website/pages/tribute');
    return { metadata, content };
}