import { DeckService } from '$lib/services/deckService';
import request from 'sync-request';
import { CardController } from '../../domain/card/cardController';
import { SuitController } from '../../domain/suit/suitController';
 
export const load = (({ params }) => {
  return {
    suits : (new SuitController((new DeckService(request)).getCards('webapp', 'en'))).getSuits(),
    cards : (new CardController((new DeckService(request)).getCards('webapp', 'en'))).getCardsFlat(),
    cardData: (new DeckService(request)).getCards('webapp', 'en'),
    mappingData: (new DeckService(request)).getCardMapping('webapp')
  };
});