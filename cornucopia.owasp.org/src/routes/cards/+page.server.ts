import { DeckService } from '$lib/services/deckService';
import { SuitController } from '../../domain/suit/suitController';
import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper';
 
export const load = (({ params }) => {
  return {
    suits : SuitController.getSuits(),
    decks :new DeckService().getCardsForAllLanguages(),
    mappingData: (new DeckService()).getCardMapping(),
    content: FileSystemHelper.getDataFromPath('data/website/pages/cards')
  };
});