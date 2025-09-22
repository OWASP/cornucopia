import {expect, describe, it} from 'vitest';
import { DeckService } from './deckService';

describe('DeckService tests', () => {
    it("should return card mapping data and call the correct url.", async () => {
        expect((new DeckService()).getCardMapping()).toBeDefined();
        DeckService.clear();
        expect((new DeckService()).getCardMapping()).toBeDefined();
        DeckService.clear();
        expect((new DeckService()).getCardMapping()).toBeDefined();
        DeckService.clear();

    });
    it("should return card deck data and call the correct url.", async () => {
        DeckService.clear();
        expect((new DeckService()).getCards('doesntexist')).toBeDefined();
        DeckService.clear();
        expect((new DeckService()).getCards('doesntexist')).toBeDefined();
        DeckService.clear();
        expect((new DeckService()).getCards('en')).toBeDefined();
        
        expect((new DeckService()).getCards('es')).toBeDefined();
        expect((new DeckService()).getCards('fr')).toBeDefined();
        expect((new DeckService()).getCards('nl')).toBeDefined();
        expect((new DeckService()).getCards('no_nb')).toBeDefined();
        expect((new DeckService()).getCards('pt_br')).toBeDefined();
        DeckService.clear();
    });

    it("should return 160 cards.", async () => {
        let cards = (new DeckService()).getCards('en');
        expect(cards.size).toBe(160);
    });
});
