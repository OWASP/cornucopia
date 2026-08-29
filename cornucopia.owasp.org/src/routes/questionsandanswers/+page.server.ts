import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper.js";
import type { PageMetadata } from "$lib/types/metadata.js";

export async function load({ params: _params }) {
    const metadata: PageMetadata = {
        title: 'Questions and Answers | OWASP Cornucopia',
        description: 'Frequently asked questions and answers about OWASP Cornucopia.',
        keywords: 'OWASP, Cornucopia, FAQ, questions, answers',
        canonicalUrl: 'https://cornucopia.owasp.org/questionsandanswers',
        type: 'website',
    };
    return { metadata, content: FileSystemHelper.getDataFromPath('data/website/pages/questionsandanswers') };
}