import { error } from "@sveltejs/kit";
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { DeckService } from "$lib/services/deckService";
import type { PageServerLoad } from "./$types";
import type { Route } from "../../../domain/routes/route";
import type { Card } from "$domain/card/card";
import { MappingService } from "$lib/services/mappingService";
import { CapecService } from "$lib/services/capecService";
import { DeckConfigService } from "$lib/services/deckConfigService";
import { getCardImagesByEdition, getSuitStylingByEdition } from "$lib/services/cardAppearanceLoader";
import { Text } from "$lib/utils/text.js";
import type { PageMetadata } from "$lib/types/metadata.js";
export const load = (async ({ params }) => {
  const lang = "en";
  const deckService = new DeckService();

  const cards = deckService.getCards(lang);
  const decks = new Map([[lang, cards]]);

  const fixedCode = legacyCardCodeFix(params.card?.toUpperCase() || "");
  const card: Card = cards.get(fixedCode) as Card;

  if (!card) {
    error(404, `Card not found: ${params.card}`);
  }

  const edition = card.edition;
  const latestVersion = DeckService.getLatestVersion(edition);
  const asvsVersion = DeckConfigService.getAsvsVersion(edition, latestVersion);

  const versions = DeckService.getVersions(edition);
  let capecData = undefined;
  if (DeckConfigService.hasCapecData(edition, latestVersion)) {
        capecData = CapecService.getCapecData(edition, latestVersion);
      }
  const metadata: PageMetadata = {
      title: `OWASP Cornucopia - ${Text.convertToTitleCase(card.suitName)} (${card.id})`,
      description: card.desc || `OWASP Cornucopia card ${card.id}`,
      keywords: `OWASP, Cornucopia, ${edition}, ${Text.convertToTitleCase(card.suitName)}, ${card.id}`,
      canonicalUrl: `https://cornucopia.owasp.org/cards/${encodeURIComponent(card.id)}`,
      type: 'website',
  };
  return {
    metadata,
    card: fixedCode,
    decks,
    versions,
    routes: new Map<string, Route[]>([
      ["ASVSRoutes", FileSystemHelper.ASVSRouteMap(asvsVersion)],
    ]),
    mappingData: new MappingService().getCardMappingForLatestEdtions(),
    languages: DeckService.getLanguagesForEditionVersion(edition, latestVersion),
    capecData,
    cardImages: getCardImagesByEdition(),
    suitStyling: getSuitStylingByEdition(),
    editionName: DeckConfigService.getFullName(edition)
  };
}) satisfies PageServerLoad;
function legacyCardCodeFix(card: string) {
  return card
    .replace("COM", "CM")
    .replace("CO", "C")
    .replace("DVE", "VE")
    .replace("AC", "AT");
}
