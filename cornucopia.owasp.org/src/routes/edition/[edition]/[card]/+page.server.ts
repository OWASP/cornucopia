import type { PageServerLoad } from './$types';
import { DeckService } from "$lib/services/deckService";
import { MappingService } from "$lib/services/mappingService";
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { error } from '@sveltejs/kit';
import type { Route } from "$domain/routes/route";

export const prerender = false;

export const load: PageServerLoad = ({ params }) => {
  const edition = params?.edition;
  const cardId = params?.card.toUpperCase();
  const version = DeckService.getLatestVersion(edition);
  const lang = 'en';

  if (!DeckService.hasEdition(edition))
    error(404, `Edition not found. Only: ${DeckService.getLatestEditions().join(", ")}`);

  const cards = new DeckService().getCardDataForEditionVersionLang(edition, version, lang);
  const card = legacyCardCodeFix(cardId);

  return {
    edition,
    card,
    version,
    lang,
    cards,
    versions: DeckService.getVersions(edition),
    languages: DeckService.getLanguages(edition),
    routes: new Map<string, Route[]>([
      ['ASVSRoutes', FileSystemHelper.ASVSRouteMap()]
    ]),
    mappingData: new MappingService().getCardMappingForLatestEdtions(),
  };

  function legacyCardCodeFix(card: string) {
    return card.replace('COM', 'CM').replace('CO', 'C').replace('DVE', 'VE').replace('AC', 'AT');
  }
};

