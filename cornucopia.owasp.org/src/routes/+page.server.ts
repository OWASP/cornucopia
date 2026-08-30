import { DeckService } from "$lib/services/deckService";
import { MappingService } from "$lib/services/mappingService";
import { SuitController } from "../domain/suit/suitController";
import type { PageMetadata } from "$lib/types/metadata.js";

export function load(event)
{
    const t = event.locals.translation;
    const fb = event.locals.fallbackTranslation;
    const metadata: PageMetadata = {
        title: t?.layout?.title ?? fb?.layout?.title ?? 'OWASP Cornucopia',
        description: t?.layout?.description ?? fb?.layout?.description ?? '',
        keywords: t?.layout?.keywords ?? fb?.layout?.keywords ?? '',
        canonicalUrl: 'https://cornucopia.owasp.org',
        type: 'website',
    };

    return {
        metadata,
        suits: SuitController.getSuits(),
        cards: (new DeckService()).getCards('en'),
        mappingData: (new MappingService()).getCardMappingForLatestEdtions()
    }
}