import { DeckService } from '$lib/services/deckService';
import { SuitController } from '../../domain/suit/suitController';
import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper';
import { MappingService } from '$lib/services/mappingService';

export const prerender = false;
 
export const load = (({ params }) => {
  const deckService = new DeckService();
  const decks = new Map<string, any>();
  const lang = 'en';
  const mobileCards = deckService.getCardDataForEditionVersionLang(
  'mobileapp', DeckService.getLatestVersion('mobileapp'), lang);
  const webappCards = deckService.getCardDataForEditionVersionLang(
    'webapp', DeckService.getLatestVersion('webapp'), lang);
  
  return {
    suits : SuitController.getSuits(),
    decks : decks.set(lang, new Map([...mobileCards, ...webappCards])),
    mappingData: (new MappingService()).getCardMappingForLatestEdtions(),
    content: FileSystemHelper.getDataFromPath('data/website/pages/cards')
  };
});
