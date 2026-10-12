import { DeckService } from '$lib/services/deckService';
import { error } from '@sveltejs/kit';
import { SuitController } from '$domain/suit/suitController';
import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper';
import { MappingService } from '$lib/services/mappingService.js';
import { DeckConfigService } from '$lib/services/deckConfigService';
import { getCardImagesByEdition, getSuitStylingByEdition } from '$lib/services/cardAppearanceLoader';
import type { PageMetadata } from "$lib/types/metadata.js";

export const load = (({ params }) => {
  const edition = params?.edition;
  if (!DeckService.hasEdition(edition)) error(
      404, 'Edition not found. Only: ' + DeckService.getLatestEditions().join(', ') + ' are supported.');

  const deckService = new DeckService();
  const version = DeckService.getLatestVersion(edition);
  const decks = new Map<string, Map<string, unknown>>();
  decks.set('en', deckService.getCardDataForEditionVersionLang(edition, version, 'en'));

  const metadata: PageMetadata = {
      title: `OWASP Cornucopia - ${edition} Edition`,
      description: `Browse the OWASP Cornucopia ${edition} edition card deck.`,
      keywords: `OWASP, Cornucopia, ${edition}, cards, security`,
      canonicalUrl: `https://cornucopia.owasp.org/edition/${encodeURIComponent(edition)}`,
      type: 'website',
  };

  return {
    metadata,
    suits: SuitController.getSuits(),
    decks,
    mappingData: (new MappingService()).getCardMappingForLatestEdtions(),
    edition: params.edition,
    content: FileSystemHelper.getDataFromPath('data/website/pages/cards'),
    cardImages: getCardImagesByEdition(),
    suitStyling: getSuitStylingByEdition(),
    browsableDecks: DeckConfigService.getBrowsableDecks(),
    currentDeck: DeckConfigService.getDeckConfig(edition)
  };
});