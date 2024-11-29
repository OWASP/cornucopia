import { DeckService } from '$lib/services/deckService';
import request from 'sync-request';
import { SuitController } from '../../domain/suit/suitController';
 
export const load = (({ params }) => {
  return {
    suits : SuitController.getSuits(),
    decks :new DeckService(request).getCardsForAllLanguages(),
    mappingData: (new DeckService(request)).getCardMapping()
  };
});