import { error, json, type RequestHandler } from '@sveltejs/kit';
import { DeckService } from '$lib/services/deckService';

interface MobileMappingApiOptions {
    component: 'mastg' | 'maswe';
    dataLoader: (edition: string, version: string) => object | null | undefined;
    missingDataMessage: string;
}

export function createMobileMappingHandler({
    component,
    dataLoader,
    missingDataMessage
}: MobileMappingApiOptions): RequestHandler {
    return ({ params }) => {
        const edition = params.edition;
        const version = params.version;

        if (!edition || !DeckService.hasEdition(edition) || edition !== 'mobileapp') {
            throw error(404, 'Edition not found. Only mobileapp is supported.');
        }

        if (!version || !DeckService.hasVersion(edition, version) || version !== '2.0') {
            throw error(404, 'Version not found for edition mobileapp. Only 2.0 is supported.');
        }

        const data = dataLoader(edition, version);

        if (!data || Object.keys(data).length === 0) {
            throw error(500, missingDataMessage);
        }

        return json({
            meta: {
                edition,
                component,
                language: 'ALL',
                version
            },
            ...data
        });
    };
}
