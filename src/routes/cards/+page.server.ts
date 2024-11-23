import { DeckService } from '$lib/services/deckService';
import request from 'sync-request';
import { SuitController } from '../../domain/suit/suitController';
 
export const load = (({ params }) => {
  let deck = new DeckService(request).getCards('en');
  return {
    suits : SuitController.getSuits(),
    cards : new DeckService(request).getCards('en'),
    cardData: deck,
    mappingData: (new DeckService(request)).getCardMapping('webapp')
  };
});