import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { DeckService } from "$lib/services/deckService";
import request from "sync-request";
import type { PageServerLoad } from "./$types";

export const load = (({ params }) => {
  return {
    card: params.card.toUpperCase(),
    decks: new DeckService(request).getCardsForAllLanguages(),
    ASVSRoutes: FileSystemHelper.ASVSRouteMap(),
    mappingData: (new DeckService(request)).getCardMapping('webapp')
  };
}) satisfies PageServerLoad;
