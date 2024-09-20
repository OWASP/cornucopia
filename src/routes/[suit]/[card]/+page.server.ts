import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { DeckService } from "$lib/services/deckService";
import request from "sync-request";
import { CardController } from "../../../domain/card/cardController";
import type { PageServerLoad } from "./$types";

export const load = (({ params }) => {
  return {
    card: (new CardController((new DeckService(request)).getCards('webapp', 'en'))).getCardBySuitAndName(params.suit, String(params.card).toUpperCase()),
    cards: (new CardController((new DeckService(request)).getCards('webapp', 'en'))).getCardsFlat(),
    ASVSRoutes: FileSystemHelper.ASVSRouteMap(),
    cardData: (new DeckService(request)).getCards('webapp', 'en'),
    mappingData: (new DeckService(request)).getCardMapping('webapp')
  };
}) satisfies PageServerLoad;
