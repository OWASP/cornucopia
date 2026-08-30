import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load(event) {
    const t = event.locals.translation;
    const fb = event.locals.fallbackTranslation;
    const metadata: PageMetadata = {
        title: t?.copi?.head?.title ?? fb?.copi?.head?.title ?? 'OWASP Cornucopia - Game Engine',
        description: t?.copi?.head?.description ?? fb?.copi?.head?.description ?? '',
        keywords: t?.copi?.head?.keywords ?? fb?.copi?.head?.keywords ?? '',
        canonicalUrl: 'https://cornucopia.owasp.org/copi',
        type: 'website',
    };
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/copi') };
}