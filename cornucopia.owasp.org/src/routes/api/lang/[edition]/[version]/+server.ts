import { json, error, type RequestHandler } from '@sveltejs/kit';
import { DeckService } from '$lib/services/deckService';

// Statically prerendered at build time
export const prerender = true;

export const GET: RequestHandler = ({ params }) => {
    const { edition, version } = params;

    if (!DeckService.hasEdition(edition)) {
        error(404, `Edition "${edition}" not found. Supported editions: ${DeckService.getLatestEditions().join(', ')}`);
    }

    if (!DeckService.hasVersion(edition, version)) {
        error(404, `Version "${version}" not found for edition "${edition}".`);
    }

    const languages = DeckService.getLanguages(edition);

    return json({
        meta: {
            edition,
            version,
            languages
        }
    });
};
