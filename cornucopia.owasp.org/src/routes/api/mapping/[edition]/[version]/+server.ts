import { json, error, type RequestHandler } from '@sveltejs/kit';
import { DeckService } from '$lib/services/deckService';
import { MappingService } from '$lib/services/mappingService';

export const prerender = true;

function toApiResponse(data: unknown): unknown {
    if (!data || typeof data !== 'object') {
        return data;
    }

    const typedData = data as {
        meta?: unknown;
        suits?: Array<{ cards?: Array<{ id?: string; [key: string]: unknown }> }>;
    };

    if (!Array.isArray(typedData.suits)) {
        return data;
    }

    const cards: Record<string, unknown> = {};

    for (const suit of typedData.suits) {
        if (!suit || !Array.isArray(suit.cards)) {
            continue;
        }

        for (const card of suit.cards) {
            if (!card || typeof card.id !== 'string' || card.id.length === 0) {
                continue;
            }

            if (!(card.id in cards)) {
                cards[card.id] = card;
            }
        }
    }

    return {
        ...(typedData.meta !== undefined ? { meta: typedData.meta } : {}),
        cards
    };
}

export const GET: RequestHandler = ({ params }) => {
    const edition = params.edition;
    const version = params.version;

    if (!DeckService.hasEdition(edition)) {
        throw error(404, 'Edition not found. Only: ' + DeckService.getLatestEditions().join(', ') + ' are supported.');
    }

    if (!DeckService.hasVersion(edition, version)) {
        throw error(404, 'Version not found for edition ' + edition + '. Only: ' + DeckService.getVersions(edition).join(', ') + ' are supported.');
    }

    const data = new MappingService().getCardMapping(edition, version);

    if (!data || Object.keys(data).length === 0) {
        throw error(500, 'No mapping data found.');
    }

    return json(toApiResponse(data));
};
