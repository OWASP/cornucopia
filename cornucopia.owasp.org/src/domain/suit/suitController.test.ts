import { describe, it, expect, beforeEach, vi } from 'vitest';
import { SuitController } from './suitController';
import { DeckService } from '$lib/services/deckService';
import type { Card } from '$domain/card/card';

vi.mock('$lib/services/deckService');

describe('SuitController tests', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    describe('getSuits', () => {
        it('groups cards into suits, preserving the order cards were inserted in', () => {
            vi.mocked(DeckService.getLatestEditions).mockReturnValue(['eop']);
            vi.mocked(DeckService.getLatestVersion).mockReturnValue('5.0');
            vi.mocked(DeckService.getLanguagesForEditionVersion).mockReturnValue(['en']);

            const cards = new Map<string, Card>([
                ['SPA', { id: 'SPA', suit: 'spoofing' } as Card],
                ['SP2', { id: 'SP2', suit: 'spoofing' } as Card],
                ['TAA', { id: 'TAA', suit: 'tampering' } as Card],
                ['SP3', { id: 'SP3', suit: 'spoofing' } as Card]
            ]);
            vi.mocked(DeckService.prototype.getCardDataForEditionVersionLang).mockReturnValue(cards);

            const suits = SuitController.getSuits().get('eop-en');

            expect(suits).toEqual([
                { name: 'spoofing', cards: ['SPA', 'SP2', 'SP3'] },
                { name: 'tampering', cards: ['TAA'] }
            ]);
        });

        it('builds one entry per edition/language combination', () => {
            vi.mocked(DeckService.getLatestEditions).mockReturnValue(['webapp']);
            vi.mocked(DeckService.getLatestVersion).mockReturnValue('3.0');
            vi.mocked(DeckService.getLanguagesForEditionVersion).mockReturnValue(['en', 'es']);
            vi.mocked(DeckService.prototype.getCardDataForEditionVersionLang).mockReturnValue(
                new Map([['VE2', { id: 'VE2', suit: 'validation' } as Card]])
            );

            const suits = SuitController.getSuits();

            expect(suits.has('webapp-en')).toBe(true);
            expect(suits.has('webapp-es')).toBe(true);
        });

        it('does not register an entry for a language with no card data', () => {
            vi.mocked(DeckService.getLatestEditions).mockReturnValue(['webapp']);
            vi.mocked(DeckService.getLatestVersion).mockReturnValue('3.0');
            vi.mocked(DeckService.getLanguagesForEditionVersion).mockReturnValue(['en']);
            vi.mocked(DeckService.prototype.getCardDataForEditionVersionLang).mockReturnValue(new Map());

            const suits = SuitController.getSuits();

            expect(suits.has('webapp-en')).toBe(false);
        });
    });
});
