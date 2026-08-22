import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { DeckService } from "$lib/services/deckService";
import type { PageServerLoad } from "./$types";
import type { Route } from "../../../domain/routes/route";
import type { Card } from "$domain/card/card";
import { MappingService } from "$lib/services/mappingService";
import { CapecService } from "$lib/services/capecService";
import { getCardImagesByEdition, getSuitStylingByEdition } from "$lib/services/cardAppearanceLoader";

export const load = (async ({ params }) => {

  const lang = "en";
  const deckService = new DeckService();

  const cards = deckService.getCards(lang);
  const decks = new Map([[lang, cards]]);

  const fixedCode = legacyCardCodeFix(params.card?.toUpperCase() || "");

  const card: Card = cards.get(fixedCode) as Card;

  if (!card) {
    throw new Error(`Card not found: ${fixedCode}`);
  }

  const edition = card.edition;
  const latestVersion = DeckService.getLatestVersion(edition);
  const asvsVersion = latestVersion === '3.0' ? '5.0' : '4.0.3';

  const versions = DeckService.getVersions(edition);
  let capecData = undefined;
  if (edition === 'webapp' && parseFloat(latestVersion) >= 3.0) {
        capecData = CapecService.getCapecData(edition, latestVersion);
      }
  return {
    card: fixedCode,
    decks: decks,
    versions: versions,
    routes: new Map<string, Route[]>([
      ["ASVSRoutes", FileSystemHelper.ASVSRouteMap(asvsVersion)],
    ]),
    mappingData: new MappingService().getCardMappingForLatestEdtions(),
    languages: DeckService.getLanguagesForEditionVersion(edition, latestVersion),
    capecData: capecData,
    cardImages: getCardImagesByEdition(),
    suitStyling: getSuitStylingByEdition()
  };

}) satisfies PageServerLoad;


function legacyCardCodeFix(card: string) {
  return card
    .replace("COM", "CM")
    .replace("CO", "C")
    .replace("DVE", "VE")
    .replace("AC", "AT");
}
