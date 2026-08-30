import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load(event) {
    const t = event.locals.translation;
    const fb = event.locals.fallbackTranslation;
    const metadata: PageMetadata = {
        title: t?.about?.head?.title ?? fb?.about?.head?.title ?? 'OWASP Cornucopia - About the Project',
        description: t?.about?.head?.description ?? fb?.about?.head?.description ?? '',
        keywords: t?.about?.head?.keywords ?? fb?.about?.head?.keywords ?? '',
        canonicalUrl: 'https://cornucopia.owasp.org/about',
        type: 'website',
    };
    const content = FileSystemHelper.getDataFromPath('data/website/pages/about');
    return { metadata, content };
}