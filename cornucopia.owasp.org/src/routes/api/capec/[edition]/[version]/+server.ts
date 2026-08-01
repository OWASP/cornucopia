import { json, error, type RequestHandler } from '@sveltejs/kit';
import { DeckService } from '$lib/services/deckService';
import { CapecService } from '$lib/services/capecService';

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

    const data = CapecService.getCapecData(edition, version);

    if (!data || Object.keys(data).length === 0) {
        throw error(500, 'No CAPEC data found.');
    }

    return json({
        meta: {
            edition,
            component: 'capec',
            language: 'ALL',
            version
        },
        ...data
    });
};