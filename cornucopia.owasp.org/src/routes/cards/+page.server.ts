import { DeckService } from '$lib/services/deckService';
import { SuitController } from '../../domain/suit/suitController';
import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper';
import { MappingService } from '$lib/services/mappingService';
import { getCardImagesByEdition, getSuitStylingByEdition } from '$lib/services/cardAppearanceLoader';

export const load = (({ params: _params }) => {
  const deckService = new DeckService();
  const lang = 'en';
  const decks = new Map<string, Map<string, unknown>>([[lang, deckService.getCards(lang)]]);

  return {
    suits: SuitController.getSuits(),
    decks: decks,
    mappingData: (new MappingService()).getCardMappingForLatestEdtions(),
    content: FileSystemHelper.getDataFromPath('data/website/pages/cards'),
    cardImages: getCardImagesByEdition(),
    suitStyling: getSuitStylingByEdition()
  };
});
