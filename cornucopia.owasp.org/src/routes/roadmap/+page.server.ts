import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load(event) {
    const t = event.locals.translation;
    const fb = event.locals.fallbackTranslation;
    const metadata: PageMetadata = {
        title: t?.roadmap?.head?.title ?? fb?.roadmap?.head?.title ?? 'OWASP Cornucopia - Roadmap',
        description: t?.roadmap?.head?.description ?? fb?.roadmap?.head?.description ?? '',
        keywords: t?.roadmap?.head?.keywords ?? fb?.roadmap?.head?.keywords ?? '',
        canonicalUrl: 'https://cornucopia.owasp.org/roadmap',
        type: 'website',
    };
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/roadmap') };
}