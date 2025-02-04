import Card from "$lib/components/deck/card.svelte";
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { DeckService } from "$lib/services/deckService";
import request from "sync-request";
import type { PageServerLoad } from "./$types";

export const load = (({ params }) => {
  return {
    card: legacyCardCodeFix(params.card.toUpperCase()),
    decks: new DeckService(request).getCardsForAllLanguages(),
    routes: new Map<string, Route[]>([
      ['ASVSRoutes', FileSystemHelper.ASVSRouteMap()]
    ]),
    mappingData: (new DeckService(request)).getCardMapping()
  };

  // Some QR code errors where done on the first printed decks. This will compensate for that.
  function legacyCardCodeFix(card: string) {
    return card.replace('COM', 'CM')
      .replace('CO', 'C')
      .replace('DVE', 'VE')
      .replace('AC', 'AT');
  }
}) satisfies PageServerLoad;
