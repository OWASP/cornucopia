import { DeckService } from '$lib/services/deckService';
import request from 'sync-request';
import { SuitController } from '../../domain/suit/suitController';
import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper';
 
export const load = (({ params }) => {
  return {
    suits : SuitController.getSuits(),
    decks :new DeckService(request).getCardsForAllLanguages(),
    mappingData: (new DeckService(request)).getCardMapping(),
    content: FileSystemHelper.getDataFromPath('data/website/pages/cards')
  };
});