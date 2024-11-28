import { DeckService } from '$lib/services/deckService';
import request from 'sync-request';
import { SuitController } from '../../domain/suit/suitController';
import { readLang } from '$lib/stores/stores';
 
export const load = (({ params }) => {
  return {
    suits : SuitController.getSuits(),
    decks :new DeckService(request).getCardsForAllLanguages(),
    mappingData: (new DeckService(request)).getCardMapping()
  };
});