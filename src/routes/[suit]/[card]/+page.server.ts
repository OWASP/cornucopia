import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { DeckService } from "$lib/services/deckService";
import { CardController } from "../../../domain/card/cardController";
import type { PageServerLoad } from "./$types";

export const load = (({ params }) => {
  return {
    card: (new CardController(DeckService.getCards('webapp', 'en'))).getCardBySuitAndName(params.suit, String(params.card).toUpperCase()),
    cards: (new CardController(DeckService.getCards('webapp', 'en'))).getCardsFlat(),
    ASVSRoutes: FileSystemHelper.ASVSRouteMap(),
    cardData: DeckService.getCards('webapp', 'en'),
    mappingData: DeckService.getCardMapping('webapp')
  };
}) satisfies PageServerLoad;
