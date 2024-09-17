import { getCardsFlat } from '../../domain/card/cardController';
import { getSuits } from '../../domain/suit/suitController';
 
export const load = (({ params }) => {
  return {
    suits : getSuits(),
    cards : getCardsFlat(),
  };
});