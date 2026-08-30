import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load(event) {
    const t = event.locals.translation;
    const fb = event.locals.fallbackTranslation;
    const metadata: PageMetadata = {
        title: t?.questionsandanswers?.head?.title ?? fb?.questionsandanswers?.head?.title ?? 'OWASP Cornucopia - Questions & Answers',
        description: t?.questionsandanswers?.head?.description ?? fb?.questionsandanswers?.head?.description ?? '',
        keywords: t?.questionsandanswers?.head?.keywords ?? fb?.questionsandanswers?.head?.keywords ?? '',
        canonicalUrl: 'https://cornucopia.owasp.org/questionsandanswers',
        type: 'website',
    };
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/questionsandanswers') };
}