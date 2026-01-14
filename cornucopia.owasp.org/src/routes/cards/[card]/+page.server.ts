import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { DeckService } from "$lib/services/deckService";
import type { PageServerLoad } from "./$types";
import type { Route } from "../../../domain/routes/route";
import type { Card } from "$domain/card/card";

export const load = (({ params }) => {
      const decks = new DeckService().getCardsForAllLanguages();
      const cards = decks.get('en') as Map<string, Card>;
      let card : Card = cards.get(legacyCardCodeFix(params.card?.toUpperCase())) as Card;
  return {
    card: legacyCardCodeFix(params.card?.toUpperCase()),
    decks: new DeckService().getCardsForAllLanguages(),
    routes: new Map<string, Route[]>([
      ['ASVSRoutes', FileSystemHelper.ASVSRouteMap()]
    ]),
    mappingData: (new DeckService()).getCardMapping(),
    languages: DeckService.getLanguages(card.edition),
  };

  // Some QR code errors where done on the first printed decks. This will compensate for that.
  function legacyCardCodeFix(card: string) {
    return card.replace('COM', 'CM')
      .replace('CO', 'C')
      .replace('DVE', 'VE')
      .replace('AC', 'AT');
  }
  
}) satisfies PageServerLoad;
