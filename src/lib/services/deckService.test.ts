import {expect, test} from 'vitest';
import { DeckService } from './deckService';

test('Test that the card mapping exist for all editions.', () => {
    expect(DeckService.getCardMapping('webapp')).toBeDefined();
    expect(DeckService.getCardMapping('mobileapp')).toBeDefined();
    expect(DeckService.getCardMapping('doesntexist')).toBeDefined();
    expect(DeckService.getCardMapping('doesntexist')).toHaveProperty('suits');
    expect(DeckService.getCardMapping('doesntexist').meta.edition).toEqual('webapp');
    expect(DeckService.getCardMapping('doesntexist').meta.version).toEqual('2.00');
});

test('Test that the cards has been defined for all supported languages.', () => {
    expect(DeckService.getCards('mobileapp', 'en')).toBeDefined();
    expect(DeckService.getCards('webapp', 'en')).toBeDefined();
    expect(DeckService.getCards('webapp', 'es')).toBeDefined();
    expect(DeckService.getCards('webapp', 'fr')).toBeDefined();
    expect(DeckService.getCards('webapp', 'nl')).toBeDefined();
    expect(DeckService.getCards('webapp', 'no_nb')).toBeDefined();
    expect(DeckService.getCards('webapp', 'pt_br')).toBeDefined();
    expect(DeckService.getCards('webapp', 'doesnotexist')).toBeDefined();
    expect(DeckService.getCards('webapp', 'doesnotexist')).toHaveProperty('suits');
    expect(DeckService.getCards('webapp', 'doesnotexist').meta.edition).toEqual('webapp');
    expect(DeckService.getCards('webapp', 'doesnotexist').meta.version).toEqual('2.00');
});