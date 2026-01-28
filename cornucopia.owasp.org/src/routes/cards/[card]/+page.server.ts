import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { DeckService } from "$lib/services/deckService";
import type { PageServerLoad } from "./$types";
import type { Route } from "../../../domain/routes/route";
import type { Card } from "$domain/card/card";
import { MappingService } from "$lib/services/mappingService";

export const load = (({ params }) => {
  const lang = 'en';
      const mobileCards = (new DeckService()).getCardDataForEditionVersionLang(
        'mobileapp', DeckService.getLatestVersion('mobileapp'), lang);
      const webappCards = (new DeckService()).getCardDataForEditionVersionLang(
        'webapp', DeckService.getLatestVersion('webapp'), lang);
      
      const cards = new Map([...mobileCards, ...webappCards]);
      const decks = new Map([['en', cards]]);
      
      let card : Card = cards.get(legacyCardCodeFix(params.card?.toUpperCase())) as Card;
  return {
    card: legacyCardCodeFix(params.card?.toUpperCase()),
    decks: decks,
    routes: new Map<string, Route[]>([
      ['ASVSRoutes', FileSystemHelper.ASVSRouteMap()]
    ]),
    mappingData: (new MappingService()).getCardMappingForLatestEdtions(),
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
