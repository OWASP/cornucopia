import {expect, describe, it} from 'vitest';
import { DeckService } from './deckService';

describe('DeckService tests', () => {
    it("should return card mapping data.", async () => {
        expect((new DeckService()).getCardMapping()).toBeDefined();
        DeckService.clear();
        expect((new DeckService()).getCardMapping()).toBeDefined();
        DeckService.clear();
        expect((new DeckService()).getCardMapping()).toBeDefined();
        DeckService.clear();
        expect((new DeckService()).getCardMappingForAllVersions().get('webapp-2.2')).toBeDefined();
        expect((new DeckService()).getCardMappingForAllVersions().get('webapp-3.0')).toBeDefined();
        expect((new DeckService()).getCardMappingForAllVersions().get('mobileapp-1.1')).toBeDefined();
        DeckService.clear();

    });
    it("should return card deck data.", async () => {
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
        expect((new DeckService()).getCardsForAllLanguages().get('en')).toBeDefined();
        expect((new DeckService()).getCardsForAllLanguages().get('doesntexist')).toBeUndefined();
        DeckService.clear();
    });

    it("should return card deck data and call the correct url.", async () => {
        DeckService.clear();
        expect((new DeckService()).getCardsForAllVersionsAndLanguages().get('3.0-doesntexist')).toBeUndefined();
        DeckService.clear();
        expect((new DeckService()).getCardsForAllVersionsAndLanguages().get('2.2-en')).toBeDefined();
        
        expect((new DeckService()).getCardsForAllVersionsAndLanguages().get('2.2-es')).toBeDefined();
        expect((new DeckService()).getCardsForAllVersionsAndLanguages().get('2.2-fr')).toBeDefined();
        expect((new DeckService()).getCardsForAllVersionsAndLanguages().get('2.2-nl')).toBeDefined();
        expect((new DeckService()).getCardsForAllVersionsAndLanguages().get('2.2-no_nb')).toBeDefined();
        expect((new DeckService()).getCardsForAllVersionsAndLanguages().get('2.2-pt_br')).toBeDefined();
        expect(Array.from((new DeckService()).getCardsForAllVersionsAndLanguages().get('3.0-en').keys()).length).toBe(80);

        DeckService.clear();
    }, 10000);

    it("should return 160 cards.", async () => {
        let cards = (new DeckService()).getCards('en');
        expect(cards.size).toBe(160);
    });
});
