import { getPageMetadata } from '$lib/utils/pageMetadata.js';
import { DeckService } from '$lib/services/deckService';
import { SuitController } from '../../domain/suit/suitController';
import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper';
import { MappingService } from '$lib/services/mappingService';
import { getCardImagesByEdition, getSuitStylingByEdition } from '$lib/services/cardAppearanceLoader';

export const load = ((_event) => {
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

  const metadata = getPageMetadata('cards', 'https://cornucopia.owasp.org/cards');

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