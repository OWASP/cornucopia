import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { DeckService } from "$lib/services/deckService";
import { error } from '@sveltejs/kit';
import type { Route } from "$domain/routes/route";
import { MappingService } from "$lib/services/mappingService";
import { CapecService } from "$lib/services/capecService";
import { DeckConfigService } from "$lib/services/deckConfigService";
import { getCardImagesByEdition, getSuitStylingByEdition } from "$lib/services/cardAppearanceLoader";

export const load = (({ params }) => {
    const edition =  params?.edition;
    const version =  params?.version;
    const requestedLang = params?.lang ?? 'en';

    const availableLanguages =DeckService.getLanguagesForEditionVersion(edition, version);

    const lang = availableLanguages.includes(requestedLang)? requestedLang: 'en';
    const asvsVersion = DeckConfigService.getAsvsVersion(edition, version);
    if (!DeckService.hasEdition(edition)) error(
      404, 'Edition not found. Only: ' + DeckService.getLatestEditions().join(', ') + ' are supported.');
    if (!DeckService.hasLanguage(edition, lang)) error(
      404, "Language not found for " + edition + ". Only: " + DeckService.getLanguages(edition).join(', ') + " are supported.");
    if (!DeckService.hasVersion(edition, version)) error(
      404, "Version not found for " + edition + ". Only: " + DeckService.getVersions(edition).join(', ') + " are supported.");

    let capecData = undefined;
    if (DeckConfigService.hasCapecData(edition, version)) {
      capecData = CapecService.getCapecData(edition, version);
    }
    
    return {
      edition: edition,
      versions: DeckService.getVersions(edition),
      lang: lang,
      card: legacyCardCodeFix(params.card.toUpperCase()),
      cards: new DeckService().getCardDataForEditionVersionLang(edition, version, lang),
      routes: new Map<string, Route[]>([
        ['ASVSRoutes', FileSystemHelper.ASVSRouteMap(asvsVersion)]
      ]),
      mappingData: new Map<string, unknown>([
        [`${edition}`, (new MappingService()).getCardMappingForAllVersions().get(`${edition}-${version}`)]
      ]),
      languages: DeckService.getLanguagesForEditionVersion(edition, version),
      capecData: capecData,
      cardImages: getCardImagesByEdition(),
      suitStyling: getSuitStylingByEdition(),
      editionName: DeckConfigService.getFullName(edition)
    };

    // Some QR code errors where done on the first printed decks. This will compensate for that.
    function legacyCardCodeFix(card: string) {
      return card.replace('COM', 'CM')
        .replace('CO', 'C')
        .replace('DVE', 'VE')
        .replace('AC', 'AT');
    }
  
}) satisfies PageServerLoad;
