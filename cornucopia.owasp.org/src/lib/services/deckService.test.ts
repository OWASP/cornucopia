/* eslint-disable @typescript-eslint/no-unsafe-call, @typescript-eslint/no-explicit-any, @typescript-eslint/no-unsafe-argument, @typescript-eslint/no-unsafe-type-assertion, @typescript-eslint/no-unsafe-member-access -- Bypassing strict typing for private cache access in tests */
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
        });

        it('should return correct latest versions', () => {
            expect(DeckService.getLatestVersion('webapp')).toBe('2.2');
        });
    });

    describe('Cache Management', () => {
        it('should return cards from cache if already populated', () => {
            const deckService = new DeckService();
            const mockCard: any = { id: 'test-card', edition: 'webapp' };
            const mockCards = new Map<string, Card>();
            mockCards.set('test-card', mockCard);

            (DeckService as any).cache.push({ lang: 'en', version: 'latest', data: mockCards });

            const result = deckService.getCards('en');
            expect(result).toBe(mockCards);
        });

        it('should clear the cache', () => {
            (DeckService as any).cache.push({ lang: 'en', data: new Map(), version: 'v1' });
            
            expect((DeckService as any).cache.length).toBe(1);
            
            DeckService.clear();
            
            expect((DeckService as any).cache.length).toBe(0);
        });
    });
});