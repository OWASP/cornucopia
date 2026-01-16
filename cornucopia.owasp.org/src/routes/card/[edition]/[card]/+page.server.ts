import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { error } from '@sveltejs/kit';
import { DeckService } from "$lib/services/deckService";
import type { Route } from "$domain/routes/route";

export const load = (({ params }) => {
    const edition =  params?.edition;
    const version =  edition == 'webapp' ? '2.2' : '1.1';
    let asvsVersion: string = "4.0.3";
    if (params.version === '3.0') asvsVersion = '5.0';
    if (!DeckService.hasEdition(edition)) error(
      404, 'Edition not found. Only: ' + DeckService.getEditions().join(', ') + ' are supported.');
    return {
      edition: edition,
      version: version,
      lang: 'en',
      card: legacyCardCodeFix(params.card.toUpperCase()),
      cards: new DeckService().getCardDataForEditionVersionLang(edition, version, 'en'),
      routes: new Map<string, Route[]>([
        ['ASVSRoutes', FileSystemHelper.ASVSRouteMap(asvsVersion)]
      ]),
      mappingData: (new DeckService()).getCardMapping(),
      languages: DeckService.getLanguages(edition)
    };

    // Some QR code errors where done on the first printed decks. This will compensate for that.
    function legacyCardCodeFix(card: string) {
      return card.replace('COM', 'CM')
        .replace('CO', 'C')
        .replace('DVE', 'VE')
        .replace('AC', 'AT');
    }
  
}) satisfies PageServerLoad;
