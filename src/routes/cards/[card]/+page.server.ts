import Card from "$lib/components/deck/card.svelte";
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { DeckService } from "$lib/services/deckService";
import request from "sync-request";
import { CardController } from "../../../domain/card/cardController";
import type { PageServerLoad } from "./$types";

export const load = (({ params }) => {
  let deck = new DeckService(request).getCards('webapp', 'en');
  
  let cardController = new CardController(deck, 'webapp', '2.00');
  let cardsFlat = cardController.getCardsFlat();
  let card = cardController.getCardById(String(params.card).toUpperCase());
  return {
    cards: cardsFlat,
    card: card,
    ASVSRoutes: FileSystemHelper.ASVSRouteMap(),
    mappingData: (new DeckService(request)).getCardMapping('webapp')
  };
}) satisfies PageServerLoad;
