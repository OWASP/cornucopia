import { DeckService } from '$lib/services/deckService';
import request from 'sync-request';
import { CardController } from '../../domain/card/cardController';
import { SuitController } from '../../domain/suit/suitController';
 
export const load = (({ params }) => {
  let deck = new DeckService(request).getCards('webapp', 'en');
  return {
    suits : (new SuitController(deck, 'webapp', '2.00')).getSuits(),
    cards : (new CardController(deck, 'webapp', '2.00')).getCardsFlat(),
    cardData: deck,
    mappingData: (new DeckService(request)).getCardMapping('webapp')
  };
});