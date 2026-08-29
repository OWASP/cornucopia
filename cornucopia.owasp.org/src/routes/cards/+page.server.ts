import { DeckService } from '$lib/services/deckService';
import { SuitController } from '../../domain/suit/suitController';
import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper';
import { MappingService } from '$lib/services/mappingService';
import { getCardImagesByEdition, getSuitStylingByEdition } from '$lib/services/cardAppearanceLoader';
import type { PageMetadata } from "$lib/types/metadata.js";

export const load = (({ params: _params }) => {
  const deckService = new DeckService();
  const decks = new Map<string, Map<string, unknown>>();
  const lang = 'en';
  const mobileCards = deckService.getCardDataForEditionVersionLang(
    'mobileapp', DeckService.getLatestVersion('mobileapp'), lang);
  const webappCards = deckService.getCardDataForEditionVersionLang(
    'webapp', DeckService.getLatestVersion('webapp'), lang);
  const companionCards = deckService.getCardDataForEditionVersionLang(
    'companion', DeckService.getLatestVersion('companion'), lang);
  const eopCards = deckService.getCardDataForEditionVersionLang(
    'eop', DeckService.getLatestVersion('eop'), lang);

  const metadata: PageMetadata = {
      title: 'Cards | OWASP Cornucopia',
      description: 'Browse all OWASP Cornucopia security requirement cards across all editions.',
      keywords: 'OWASP, Cornucopia, cards, security, requirements',
      canonicalUrl: 'https://cornucopia.owasp.org/cards',
      type: 'website',
  };

  return {
    metadata,
    suits: SuitController.getSuits(),
    decks: decks.set(lang, new Map([...mobileCards, ...webappCards, ...companionCards, ...eopCards])),
    mappingData: (new MappingService()).getCardMappingForLatestEdtions(),
    content: FileSystemHelper.getDataFromPath('data/website/pages/cards'),
    cardImages: getCardImagesByEdition(),
    suitStyling: getSuitStylingByEdition()
  };
});