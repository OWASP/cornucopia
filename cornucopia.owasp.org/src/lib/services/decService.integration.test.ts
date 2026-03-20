 
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { DeckService } from './deckService';

describe('DeckService integration tests', () => {
  const service = new DeckService();

  // Expected sizes based on current data
  const EXPECTED = {
    EDITION_SIZE: 80,
    TOTAL_EN_SIZE: 251
  };

  beforeEach(() => {
    DeckService.clear();
  });

  afterEach(() => {
    DeckService.clear();
  });

  it("should return card deck data for various languages", () => {
    expect(service.getCards('doesntexist')).toBeDefined();
    expect(service.getCards('en')).toBeDefined();
    expect(service.getCards('es')).toBeDefined();
    expect(service.getCards('fr')).toBeDefined();
    expect(service.getCards('nl')).toBeDefined();
    expect(service.getCards('no_nb')).toBeDefined();
    expect(service.getCards('pt_br')).toBeDefined();
  });

  it("should get Card data for specific edition, version and lang", () => {
    // Basic existence checks
    expect(service.getCardDataForEditionVersionLang('webapp', '2.2', 'en')).toBeDefined();
    expect(service.getCardDataForEditionVersionLang('webapp', '3.0', 'ru')).toBeDefined();
    expect(service.getCardDataForEditionVersionLang('mobileapp', '1.1', 'en')).toBeDefined();
    expect(service.getCardDataForEditionVersionLang('companion', '1.0', 'en')).toBeDefined();

    // Size verification
    expect(service.getCardDataForEditionVersionLang('webapp', '2.2', 'en').size).toBe(EXPECTED.EDITION_SIZE);
    expect(service.getCardDataForEditionVersionLang('webapp', '3.0', 'ru').size).toBe(EXPECTED.EDITION_SIZE);
    expect(service.getCardDataForEditionVersionLang('webapp', '3.0', 'en').size).toBe(EXPECTED.EDITION_SIZE);
    expect(service.getCardDataForEditionVersionLang('mobileapp', '1.1', 'en').size).toBe(EXPECTED.EDITION_SIZE);
    expect(service.getCardDataForEditionVersionLang('webapp', '2.2', 'it').size).toBe(EXPECTED.EDITION_SIZE);
    expect(service.getCardDataForEditionVersionLang('webapp', '2.2', 'es').size).toBe(EXPECTED.EDITION_SIZE);
  });

  it("should return the correct total count of English cards", () => {
    const cards = service.getCards('en');
    expect(cards.size).toBe(EXPECTED.TOTAL_EN_SIZE);
  });
});