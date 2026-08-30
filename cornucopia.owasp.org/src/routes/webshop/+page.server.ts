import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load(event) {
    const t = event.locals.translation;
    const fb = event.locals.fallbackTranslation;
    const metadata: PageMetadata = {
        title: t?.webshop?.head?.title ?? fb?.webshop?.head?.title ?? 'OWASP Cornucopia - Webshop',
        description: t?.webshop?.head?.description ?? fb?.webshop?.head?.description ?? '',
        keywords: t?.webshop?.head?.keywords ?? fb?.webshop?.head?.keywords ?? '',
        canonicalUrl: 'https://cornucopia.owasp.org/webshop',
        type: 'website',
    };
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/webshop') };
}