import Card from "$lib/components/deck/card.svelte";
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { DeckService } from "$lib/services/deckService";
import request from "sync-request";
import type { PageServerLoad } from "./$types";

export const load = (({ params }) => {
  return {
    decks: new DeckService(request).getCardsForAllLanguages(),
    card: params.card.toUpperCase(),
    ASVSRoutes: FileSystemHelper.ASVSRouteMap(),
    mappingData: (new DeckService(request)).getCardMapping('webapp')
  };
}) satisfies PageServerLoad;
