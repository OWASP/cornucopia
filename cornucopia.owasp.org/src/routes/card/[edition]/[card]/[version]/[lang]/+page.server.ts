import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { DeckService } from "$lib/services/deckService";
import { error } from '@sveltejs/kit';
import type { Route } from "$domain/routes/route";

export const load = (({ params }) => {
    const edition =  params?.edition;
    const version =  params?.version;
    const lang =  params?.lang;
    let asvsVersion: string = "4.0.3";
    if (params.version === '3.0') asvsVersion = '5.0';
    if (!DeckService.hasEdition(edition)) error(
      404, 'Edition not found. Only: ' + DeckService.getEditions().join(', ') + ' are supported.');
    if (!DeckService.hasLanguage(edition, lang)) error(
      404, "Language not found for " + edition + ". Only: " + DeckService.getLanguages(edition).join(', ') + " are supported.");
    if (!DeckService.hasVersion(edition, version)) error(
      404, "Version not found for " + edition + ". Only: " + DeckService.getVersions(edition).join(', ') + " are supported.");
    return {
      edition: edition,
      version: version,
      lang: lang,
      card: legacyCardCodeFix(params.card.toUpperCase()),
      cards: new DeckService().getCardDataForEditionVersionLang(edition, version, lang),
      routes: new Map<string, Route[]>([
        ['ASVSRoutes', FileSystemHelper.ASVSRouteMap(asvsVersion)]
      ]),
      mappingData: new Map<string, any>([
        [`${edition}`, (new DeckService()).getCardMappingForAllVersions().get(`${edition}-${version}`)]
      ]),
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
