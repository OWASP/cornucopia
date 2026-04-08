import { json, error, type RequestHandler } from '@sveltejs/kit';
import { DeckService } from '$lib/services/deckService';
import { AsvsService } from '$lib/services/asvsService';

export const prerender = true;

export const GET: RequestHandler = ({ params }) => {
    const edition = params.edition;
    const version = params.version;

    if (!edition || !DeckService.hasEdition(edition)) {
        throw error(404, 'Edition not found. Only: ' + DeckService.getLatestEditions().join(', ') + ' are supported.');
    }

    if (!version || !DeckService.hasVersion(edition, version)) {
        throw error(404, 'Version not found for edition ' + edition + '. Only: ' + DeckService.getVersions(edition).join(', ') + ' are supported.');
    }

    const data = AsvsService.getAsvsData(edition, version);

    if (!data || Object.keys(data).length === 0) {
        throw error(500, 'No ASVS data found.');
    }

    return json({
        meta: {
            edition,
            component: 'asvs',
            language: 'ALL',
            version
        },
        ...data
    });
};