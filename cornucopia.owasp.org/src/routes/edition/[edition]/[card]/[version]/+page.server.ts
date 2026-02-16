import type { PageServerLoad } from './$types';
import { DeckService } from "$lib/services/deckService";
import { MappingService } from "$lib/services/mappingService";
import { CapecService } from "$lib/services/capecService";
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { error } from '@sveltejs/kit';
import type { Route } from "$domain/routes/route";

export const load: PageServerLoad = ({ params }) => {
  const edition = params?.edition;
  const cardId = params?.card.toUpperCase();
  const version = params?.version || DeckService.getLatestVersion(edition);
  const lang = 'en';

  if (!DeckService.hasEdition(edition))
    error(404, `Edition not found. Only: ${DeckService.getLatestEditions().join(", ")}`);

  if (!DeckService.hasVersion(edition, version))
    error(404, `Version not found for ${edition}. Only: ${DeckService.getVersions(edition).join(", ")}`);

  const cards = new DeckService().getCardDataForEditionVersionLang(edition, version, lang);
  const card = legacyCardCodeFix(cardId);

  const capecData = edition === 'webapp' && parseFloat(version) >= 3.0
    ? CapecService.getCapecData(edition, version)
    : undefined;

  let asvsVersion = version === '3.0' ? '5.0' : '4.0.3';

  return {
    edition,
    card,
    version,
    lang,
    cards,
    versions: DeckService.getVersions(edition),
    languages: DeckService.getLanguages(edition),
    routes: new Map<string, Route[]>([
      ['ASVSRoutes', FileSystemHelper.ASVSRouteMap(asvsVersion)]
    ]),
    mappingData: new Map<string, any>([
      [edition, (new MappingService()).getCardMappingForAllVersions().get(`${edition}-${version}`)]
    ]),
    capecData
  };

  function legacyCardCodeFix(card: string) {
    return card.replace('COM', 'CM').replace('CO', 'C').replace('DVE', 'VE').replace('AC', 'AT');
  }
};

