import { getPageMetadata } from '$lib/utils/pageMetadata.js';
import { DeckService } from "$lib/services/deckService";
import { MappingService } from "$lib/services/mappingService";
import { SuitController } from "../domain/suit/suitController";

export function load(_event)
{
    const metadata = getPageMetadata(_event, 'home', 'https://cornucopia.owasp.org');

    return {
        metadata,
        suits: SuitController.getSuits(),
        cards: (new DeckService()).getCards('en'),
        mappingData: (new MappingService()).getCardMappingForLatestEdtions()
    }
}