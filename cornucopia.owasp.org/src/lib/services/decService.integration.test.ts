import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { DeckService } from './deckService';

describe('DeckService integration tests', () => {
    beforeEach(() => {
        DeckService.clear();
    });

    afterEach(() => {
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
    });

    it("should get Card data for edition, version and lang.", async () => {
        expect((new DeckService()).getCardDataForEditionVersionLang('webapp', '2.2', 'en')).toBeDefined();
        expect((new DeckService()).getCardDataForEditionVersionLang('webapp', '3.0', 'ru')).toBeDefined();
        expect((new DeckService()).getCardDataForEditionVersionLang('webapp', '3.0', 'en')).toBeDefined();
        expect((new DeckService()).getCardDataForEditionVersionLang('webapp', '2.2', 'it')).toBeDefined();
        expect((new DeckService()).getCardDataForEditionVersionLang('webapp', '2.2', 'es')).toBeDefined();
        expect((new DeckService()).getCardDataForEditionVersionLang('webapp', '2.2', 'fr')).toBeDefined();
        expect((new DeckService()).getCardDataForEditionVersionLang('webapp', '2.2', 'nl')).toBeDefined();
        expect((new DeckService()).getCardDataForEditionVersionLang('webapp', '2.2', 'no_nb')).toBeDefined();
        expect((new DeckService()).getCardDataForEditionVersionLang('webapp', '2.2', 'pt_br')).toBeDefined();
        expect((new DeckService()).getCardDataForEditionVersionLang('webapp', '2.2', 'pt_pt')).toBeDefined();

        expect((new DeckService()).getCardDataForEditionVersionLang('mobileapp', '1.1', 'en')).toBeDefined();

        expect((new DeckService()).getCardDataForEditionVersionLang('webapp', '2.2', 'en').size).toBe(80);
        expect((new DeckService()).getCardDataForEditionVersionLang('webapp', '3.0', 'ru').size).toBe(80);
        expect((new DeckService()).getCardDataForEditionVersionLang('webapp', '3.0', 'en').size).toBe(80);
        expect((new DeckService()).getCardDataForEditionVersionLang('mobileapp', '1.1', 'en').size).toBe(80);
        expect((new DeckService()).getCardDataForEditionVersionLang('webapp', '2.2', 'it').size).toBe(80);
        expect((new DeckService()).getCardDataForEditionVersionLang('webapp', '2.2', 'es').size).toBe(80);
        expect((new DeckService()).getCardDataForEditionVersionLang('webapp', '2.2', 'fr').size).toBe(80);
        expect((new DeckService()).getCardDataForEditionVersionLang('webapp', '2.2', 'nl').size).toBe(80);
        expect((new DeckService()).getCardDataForEditionVersionLang('webapp', '2.2', 'no_nb').size).toBe(80);
        expect((new DeckService()).getCardDataForEditionVersionLang('webapp', '2.2', 'pt_br').size).toBe(80);
        expect((new DeckService()).getCardDataForEditionVersionLang('webapp', '2.2', 'pt_pt').size).toBe(80);
    });

    it("should return 160 cards.", async () => {
        let cards = (new DeckService()).getCards('en');
        expect(cards.size).toBe(160);
    });
});
