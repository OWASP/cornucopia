/* eslint-disable import/enforce-node-protocol-usage, @typescript-eslint/init-declarations, @typescript-eslint/consistent-type-assertions, @typescript-eslint/no-unsafe-type-assertion, @typescript-eslint/dot-notation, @typescript-eslint/no-unsafe-argument, @typescript-eslint/no-explicit-any, max-nested-callbacks, max-lines -- Bypassing strict stylistic rules for legacy test file */
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { DeckService } from './deckService';
import type { Card } from '$domain/card/card';

describe('DeckService Unit Tests', () => {
    beforeEach(() => {
        DeckService.clear();
        vi.clearAllMocks();
    });

    afterEach(() => {
        DeckService.clear();
    });

    describe('Static Metadata Logic', () => {
        it('should validate known editions', () => {
            expect(DeckService.hasEdition('webapp')).toBe(true);
            expect(DeckService.hasEdition('mobileapp')).toBe(true);
            expect(DeckService.hasEdition('unknown')).toBe(false);
        });

        it('should validate known versions', () => {
            expect(DeckService.hasVersion('webapp', '3.0')).toBe(true);
            expect(DeckService.hasVersion('mobileapp', '1.1')).toBe(true);
            expect(DeckService.hasVersion('webapp', '1.0')).toBe(false);
        });

        it('should return correct latest versions', () => {
            expect(DeckService.getLatestVersion('webapp')).toBe('2.2');
            expect(DeckService.getLatestVersion('mobileapp')).toBe('1.1');
        });

        it('should return all available languages for an edition', () => {
            const languages = DeckService.getLanguages('webapp');
            expect(languages).toContain('en');
            expect(languages).toContain('es');
            expect(languages).toContain('ru');
        });
    });

    describe('Cache Management', () => {
        it('should return cards from cache if already populated', () => {
            const deckService = new DeckService();
            const mockCards = new Map<string, Card>();
            mockCards.set('test-card', { id: 'test-card', edition: 'webapp' } as Card);

            // Directly inject into the private cache to test the cache-retrieval branch
            DeckService['cache'].push({ lang: 'en', version: 'latest', data: mockCards });

            const result = deckService.getCards('en');
            expect(result).toBe(mockCards);
            expect(result.size).toBe(1);
        });

        it('should clear the cache on command', () => {
            DeckService['cache'].push({ lang: 'en', data: new Map(), version: 'v1' });
            expect(DeckService['cache'].length).toBe(1);
            
            DeckService.clear();
            expect(DeckService['cache'].length).toBe(0);
        });
    });
});