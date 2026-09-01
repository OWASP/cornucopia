import en from '$lib/translations/en/index.js';
import type { PageMetadata } from '$lib/types/metadata.js';

type TranslationRecord = Record<string, unknown>;
type MetadataEvent = {
    locals?: {
        translation?: unknown;
        fallbackTranslation?: unknown;
    };
};

const isRecord = (value: unknown): value is TranslationRecord =>
    typeof value === 'object' && value !== null;

const getText = (
    source: unknown,
    section: string,
    field: 'title' | 'description' | 'keywords',
    useHead: boolean,
): string | undefined => {
    if (!isRecord(source)) return undefined;

    const sectionValue = source[section];
    if (!isRecord(sectionValue)) return undefined;

    const value = useHead ? sectionValue.head : sectionValue;
    if (!isRecord(value)) return undefined;

    const text = value[field];
    return typeof text === 'string' && text.trim() ? text : undefined;
};

export const getPageMetadata = (
    event: MetadataEvent,
    section: string,
    canonicalUrl: string,
    useHead = true,
): PageMetadata => {
    const sources = [
        event.locals?.translation,
        event.locals?.fallbackTranslation,
        en,
    ];
    const read = (field: 'title' | 'description' | 'keywords') =>
        sources
            .map((source) => getText(source, section, field, useHead))
            .find((text): text is string => Boolean(text));

    return {
        title: read('title') ?? 'OWASP Cornucopia',
        description: read('description') ?? 'OWASP Cornucopia',
        keywords: read('keywords') ?? 'OWASP, Cornucopia',
        canonicalUrl,
        type: 'website',
    };
};
