import { DeckService } from "$lib/services/deckService";
import { MappingService } from "$lib/services/mappingService";
import { CapecService } from "$lib/services/capecService";
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { error, redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
import type { Route } from "$domain/routes/route";
import type { Card } from "$domain/card/card";

export const prerender = false;

export const load: PageServerLoad = ({ params }) => {
  // Extract route params
  let edition = params.edition || "webapp"; // fallback for old URLs
  const cardIdRaw = params.card;
  const version = params.version || DeckService.getLatestVersion(edition);
  const lang = params.lang || "en";

  if (!cardIdRaw) throw error(404, "Card not specified");

  const cardId = fixLegacyCardId(cardIdRaw.toUpperCase());

// Validate language with fallback to English
let resolvedLang = lang;

if (!DeckService.hasLanguage(edition, resolvedLang)) {
  resolvedLang = "en";
}

  // Check version exists
  if (!DeckService.hasVersion(edition, version)) {
    throw error(404, `Version not found for ${edition}. Available: ${DeckService.getVersions(edition).join(", ")}`);
  }

  // Check language exists
  if (!DeckService.hasLanguage(edition, lang)) {
    throw error(404, `Language not found for ${edition}. Available: ${DeckService.getLanguages(edition).join(", ")}`);
  }

  // Fetch card data
let cards = new DeckService().getCardDataForEditionVersionLang(edition, version, resolvedLang);

// If card missing in requested language, fallback to English
if (!cards.has(cardId) && resolvedLang !== "en") {
  resolvedLang = "en";
  cards = new DeckService().getCardDataForEditionVersionLang(edition, version, resolvedLang);
}

  const card = cards.get(cardId) as Card;

  if (!card) {
    throw error(404, `Card ${cardId} not found in edition ${edition}`);
  }

  // Load CAPEC data if needed
  const capecData = edition === "webapp" && parseFloat(version) >= 3.0
    ? CapecService.getCapecData(edition, version)
    : undefined;

  // ASVS routes
  const asvsVersion = version === "3.0" ? "5.0" : "4.0.3";
  const routes = new Map<string, Route[]>([['ASVSRoutes', FileSystemHelper.ASVSRouteMap(asvsVersion)]]);

  // Mapping data
  const mappingData = new Map<string, any>([
    [edition, new MappingService().getCardMappingForAllVersions().get(`${edition}-${version}`)]
  ]);

  return {
    edition,
    card: cardId,
    version,
    lang: resolvedLang,
    cards,
    versions: DeckService.getVersions(edition),
    languages: DeckService.getLanguages(edition),
    routes,
    mappingData,
    capecData
  };
};

// Fix old card codes to new format
function fixLegacyCardId(card: string) {
  return card.replace("COM", "CM")
             .replace("CO", "C")
             .replace("DVE", "VE")
             .replace("AC", "AT");
}

