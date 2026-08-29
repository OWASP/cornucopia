import { DeckService } from "$lib/services/deckService";
import { MappingService } from "$lib/services/mappingService";
import { SuitController } from "../domain/suit/suitController";
import type { PageMetadata } from "$lib/types/metadata.js";

export function load()
{
    const metadata: PageMetadata = {
        title: 'OWASP Cornucopia',
        description: 'OWASP Cornucopia is a mechanism in the form of a card game to assist software development teams identify security requirements in Agile, conventional and formal development processes.',
        keywords: 'OWASP, Cornucopia, security, card game, threat modeling',
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