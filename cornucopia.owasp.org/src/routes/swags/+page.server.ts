import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load(event) {
    const t = event.locals.translation;
    const fb = event.locals.fallbackTranslation;
    const metadata: PageMetadata = {
        title: t?.swags?.head?.title ?? fb?.swags?.head?.title ?? 'OWASP Cornucopia - Swags and logos',
        description: t?.swags?.head?.description ?? fb?.swags?.head?.description ?? '',
        keywords: t?.swags?.head?.keywords ?? fb?.swags?.head?.keywords ?? '',
        canonicalUrl: 'https://cornucopia.owasp.org/swags',
        type: 'website',
    };
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/swags') };
}