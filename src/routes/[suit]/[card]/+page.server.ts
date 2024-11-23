import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { DeckService } from "$lib/services/deckService";
import request from "sync-request";
import type { PageServerLoad } from "./$types";

export const load = (({ params }) => {
  let cards = new DeckService(request).getCards('en');
  return {
    card: cards.get(String(params.card).toUpperCase()),
    cards: cards,
    ASVSRoutes: FileSystemHelper.ASVSRouteMap(),
    mappingData: (new DeckService(request)).getCardMapping('webapp')
  };
}) satisfies PageServerLoad;
