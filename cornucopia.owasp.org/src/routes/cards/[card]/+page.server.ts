import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { DeckService } from "$lib/services/deckService";
import type { PageServerLoad } from "./$types";
import type { Route } from "../../../domain/routes/route";
import type { Card } from "$domain/card/card";
import { MappingService } from "$lib/services/mappingService";

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

  const cards = new Map([...mobileCards, ...webappCards]);
  const decks = new Map([["en", cards]]);

  const fixedCode = legacyCardCodeFix(params.card?.toUpperCase() || "");

  const card: Card = cards.get(fixedCode) as Card;

  if (!card) {
    throw new Error(`Card not found: ${fixedCode}`);
  }

  const edition = card.edition;

  const versions = DeckService.getVersions(edition);

  return {
    card: fixedCode,
    decks: decks,
    versions: versions,
    routes: new Map<string, Route[]>([
      ["ASVSRoutes", FileSystemHelper.ASVSRouteMap()],
    ]),
    mappingData: new MappingService().getCardMappingForLatestEdtions(),
    languages: DeckService.getLanguages(card.edition),
  };

}) satisfies PageServerLoad;


function legacyCardCodeFix(card: string) {
  return card
    .replace("COM", "CM")
    .replace("CO", "C")
    .replace("DVE", "VE")
    .replace("AC", "AT");
}
