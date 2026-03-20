import { DeckService } from '$lib/services/deckService';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = () => {
  const service = new DeckService();
  const lang = 'en';
  const cards = service.getCards(lang);

  // Convert Map to a plain object for the frontend to handle safely
  const cardList = Array.from(cards.values());

  return {
    cards: cardList,
    totalCount: cardList.length
  };
};