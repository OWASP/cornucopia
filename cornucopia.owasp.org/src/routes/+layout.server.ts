import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper';
import { Text } from '$lib/utils/text.js';
import { DeckService } from '$lib/services/deckService';
import { CardImagesService } from '$lib/services/cardImagesService';
import { SuitStylingService } from '$lib/services/suitStylingService';

export const prerender = true;
export async function load(event) 
{
    const content = FileSystemHelper.getDataFromPath('data/website/pages/footer');
    const eopVersion = DeckService.getLatestVersion('eop');
    return {
        content: content,
        renderTimestamp : Text.FormatDateAsDate(new Date()),
        timestamp : new Date(),
        translation: event.locals.translation,
        fallbackTranslation: event.locals.fallbackTranslation,
        lang: event.locals.lang,
        cardImages: (new CardImagesService()).getCardImages('eop', eopVersion),
        suitStyling: (new SuitStylingService()).getSuitStyling('eop', eopVersion)
    }
}