import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper';
import { Text } from '$lib/utils/text.js';
import { DeckService } from '$lib/services/deckService';
import { CardImagesService } from '$lib/services/cardImagesService';
import { SuitStylingService } from '$lib/services/suitStylingService';
import type { CardImage } from '$lib/services/cardImagesService';
import type { SuitStyling } from '$lib/services/suitStylingService';

export const prerender = true;

// Used edition as a key so future decks can add their own yaml.
function getCardImagesByEdition(): Record<string, Record<string, CardImage>> {
    const service = new CardImagesService();
    const result: Record<string, Record<string, CardImage>> = {};
    for (const edition of DeckService.getLatestEditions()) {
        const images = service.getCardImages(edition, DeckService.getLatestVersion(edition));
        if (images) result[edition] = images;
    }
    return result;
}

function getSuitStylingByEdition(): Record<string, Record<string, SuitStyling>> {
    const service = new SuitStylingService();
    const result: Record<string, Record<string, SuitStyling>> = {};
    for (const edition of DeckService.getLatestEditions()) {
        const styling = service.getSuitStyling(edition, DeckService.getLatestVersion(edition));
        if (styling) result[edition] = styling;
    }
    return result;
}

export async function load(event)
{
    const content = FileSystemHelper.getDataFromPath('data/website/pages/footer');
    return {
        content: content,
        renderTimestamp : Text.FormatDateAsDate(new Date()),
        timestamp : new Date(),
        translation: event.locals.translation,
        fallbackTranslation: event.locals.fallbackTranslation,
        lang: event.locals.lang,
        cardImages: getCardImagesByEdition(),
        suitStyling: getSuitStylingByEdition()
    }
}