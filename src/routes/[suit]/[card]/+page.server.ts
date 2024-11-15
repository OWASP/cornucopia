import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { DeckService } from "$lib/services/deckService";
import request from "sync-request";
import { CardController } from "../../../domain/card/cardController";
import type { PageServerLoad } from "./$types";

export const load = (({ params }) => {
  return {
    card: (new CardController((new DeckService(request)).getCards('webapp', 'en'), 'webapp', '2.00')).getCardById(String(params.card).toUpperCase()),
    cards: (new CardController((new DeckService(request)).getCards('webapp', 'en'), 'webapp', '2.00')).getCardsFlat(),
    ASVSRoutes: FileSystemHelper.ASVSRouteMap(),
    mappingData: (new DeckService(request)).getCardMapping('webapp')
  };
}) satisfies PageServerLoad;
