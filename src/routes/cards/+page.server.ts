import { DeckService } from '$lib/services/deckService';
import { CardController } from '../../domain/card/cardController';
import { SuitController } from '../../domain/suit/suitController';
 
export const load = (({ params }) => {
  return {
    suits : (new SuitController(DeckService.getCards('webapp', 'en'))).getSuits(),
    cards : (new CardController(DeckService.getCards('webapp', 'en'))).getCardsFlat(),
    cardData: DeckService.getCards('webapp', 'en'),
    mappingData: DeckService.getCardMapping('webapp')
  };
});