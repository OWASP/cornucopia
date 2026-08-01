import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { DeckService } from "$lib/services/deckService";
import type { PageServerLoad } from "./$types";
import type { Route } from "../../../domain/routes/route";
import type { Card } from "$domain/card/card";
import { MappingService } from "$lib/services/mappingService";
import { CapecService } from "$lib/services/capecService";

export const load = (async ({ params }) => {

  const lang = "en";
  const deckService = new DeckService();

  const mobileCards = deckService.getCardDataForEditionVersionLang(
    "mobileapp",
    DeckService.getLatestVersion("mobileapp"),
    lang
  );

  const webappCards = deckService.getCardDataForEditionVersionLang(
    "webapp",
    DeckService.getLatestVersion("webapp"),
    lang
  );

  const companionCards = deckService.getCardDataForEditionVersionLang(
    "companion",
    DeckService.getLatestVersion("companion"),
    lang
  );

  const eopCards = deckService.getCardDataForEditionVersionLang(
    "eop",
    DeckService.getLatestVersion("eop"),
    lang
  );

  const cards = new Map([...mobileCards, ...webappCards, ...companionCards, ...eopCards]);
  const decks = new Map([["en", cards]]);

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
    capecData: capecData
  };

}) satisfies PageServerLoad;


function legacyCardCodeFix(card: string) {
  return card
    .replace("COM", "CM")
    .replace("CO", "C")
    .replace("DVE", "VE")
    .replace("AC", "AT");
}
