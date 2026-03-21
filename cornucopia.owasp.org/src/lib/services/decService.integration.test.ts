import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { DeckService } from './deckService';

describe('DeckService Integration & Coverage', () => {
    beforeEach(() => {
        DeckService.clear();
    });

    afterEach(() => {
        DeckService.clear();
    });

    it("should cover all card loading and parsing branches", () => {
        const service = new DeckService();
        
        // 1. Test standard loading (Hits main parsing logic)
        const enCards = service.getCards('en');
        expect(enCards.size).toBeGreaterThan(0);

        // 2. Test cache hits (Hits the 'if (cached)' branch)
        const cachedCards = service.getCards('en');
        expect(cachedCards).toBe(enCards);

        // 3. Test edge case: Edition/Version/Lang specific (Hits line 123, 133+)
        const specific = service.getCardDataForEditionVersionLang('webapp', '3.0', 'en');
        expect(specific.size).toBeGreaterThan(0);
    }, 30000);

    it("should handle missing files and error branches", () => {
        const service = new DeckService();
        
        // 1. Test non-existent language (Hits the error/empty return branches)
        const invalid = service.getCardDataForEditionVersionLang('webapp', '2.2', 'not-a-lang');
        expect(invalid.size).toBe(0);

        // 2. Test non-existent edition
        const noEdition = service.getCardDataForEditionVersionLang('fake-edition', '1.0', 'en');
        expect(noEdition.size).toBe(0);
    });

    it("should cover static helper methods", () => {
        // Hits the metadata branches (hasEdition, getLatestVersion, etc.)
        expect(DeckService.hasEdition('webapp')).toBe(true);
        expect(DeckService.hasVersion('webapp', '3.0')).toBe(true);
        expect(DeckService.getLatestVersion('webapp')).toBe('2.2');
        expect(DeckService.getLanguages('webapp')).toContain('en');
    });
});