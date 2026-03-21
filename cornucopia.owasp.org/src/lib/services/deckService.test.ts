/* eslint-disable import/enforce-node-protocol-usage, @typescript-eslint/init-declarations, @typescript-eslint/consistent-type-assertions, @typescript-eslint/no-unsafe-type-assertion, @typescript-eslint/dot-notation, @typescript-eslint/no-unsafe-argument, @typescript-eslint/no-explicit-any, max-nested-callbacks, max-lines -- Bypassing strict stylistic rules for legacy test file */
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { DeckService } from './deckService';
import type { Card } from '$domain/card/card';
import fs from 'fs';
import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper';
import { MappingService } from './mappingService';

// 1. TOP-LEVEL MOCKS
vi.mock('fs');
vi.mock('$lib/filesystem/fileSystemHelper');
vi.mock('./mappingService');

// Global setup for FileSystemHelper to prevent early exits
vi.mocked(FileSystemHelper.hasFile).mockReturnValue(true);
vi.mocked(FileSystemHelper.hasDir).mockReturnValue(true);

describe('DeckService tests', () => {
    beforeEach(() => {
        DeckService.clear();
        vi.clearAllMocks();
        // Reset defaults after each clear
        vi.mocked(FileSystemHelper.hasFile).mockReturnValue(true);
        vi.mocked(FileSystemHelper.hasDir).mockReturnValue(true);
    });

    afterEach(() => {
        DeckService.clear();
    });

    describe('hasEdition', () => {
        it('should return true for webapp edition', () => {
            expect(DeckService.hasEdition('webapp')).toBe(true);
        });
        it('should return true for mobileapp edition', () => {
            expect(DeckService.hasEdition('mobileapp')).toBe(true);
        });
        it('should return true for companion edition', () => {
            expect(DeckService.hasEdition('companion')).toBe(true);
        });
        it('should return false for unknown edition', () => {
            expect(DeckService.hasEdition('unknown')).toBe(false);
        });
        it('should return false for empty string', () => {
            expect(DeckService.hasEdition('')).toBe(false);
        });
    }, 10000);

    describe('hasVersion', () => {
        it('should return true for webapp version 2.2', () => {
            expect(DeckService.hasVersion('webapp', '2.2')).toBe(true);
        });
        it('should return true for webapp version 3.0', () => {
            expect(DeckService.hasVersion('webapp', '3.0')).toBe(true);
        });
        it('should return true for mobileapp version 1.1', () => {
            expect(DeckService.hasVersion('mobileapp', '1.1')).toBe(true);
        });
        it('should return true for companion version 1.0', () => {
            expect(DeckService.hasVersion('companion', '1.0')).toBe(true);
        });
        it('should return false for invalid version', () => {
            expect(DeckService.hasVersion('webapp', '1.0')).toBe(false);
        });
    }, 10000);

    describe('hasLanguage', () => {
        it('should return true for webapp with en', () => {
            expect(DeckService.hasLanguage('webapp', 'en')).toBe(true);
        });
        it('should return true for mobileapp with en', () => {
            expect(DeckService.hasLanguage('mobileapp', 'en')).toBe(true);
        });
        it('should return true for companion with en', () => {
            expect(DeckService.hasLanguage('companion', 'en')).toBe(true);
        });
        it('should return false for mobileapp with es', () => {
            expect(DeckService.hasLanguage('mobileapp', 'es')).toBe(false);
        });
    }, 10000);

    describe('getDecks', () => {
        it('should return all available decks', () => {
            const decks = DeckService.getDecks();
            expect(decks).toHaveLength(4);
        });
    }, 10000);

    describe('getLatestVersion', () => {
        it('should return 2.2 for webapp', () => {
            expect(DeckService.getLatestVersion('webapp')).toBe('2.2');
        });
    }, 10000);

    describe('getLatestEditions', () => {
        it('should return array of latest editions', () => {
            const editions = DeckService.getLatestEditions();
            expect(editions).toHaveLength(3);
        });
    }, 10000);

    describe('getLanguages', () => {
        it('should return all languages for webapp', () => {
            const languages = DeckService.getLanguages('webapp');
            expect(languages).toContain('en');
        });
    }, 10000);

    describe('getCards', () => {
        let deckService: DeckService;
        beforeEach(() => { deckService = new DeckService(); });

        it('should return cards from cache if available', () => {
            const mockCards = new Map<string, Card>();
            mockCards.set('card1', { id: 'card1', edition: 'webapp' } as Card);
            DeckService['cache'].push({ lang: 'en', version: 'latest', data: mockCards });
            const result = deckService.getCards('en');
            expect(result.size).toBe(1);
        });

        it('should load cards if not in cache', () => {
            const mockYaml = 'suits:\n  - id: s1\n    name: S1\n    cards:\n      - id: c1\n        value: A\n        desc: D';
            vi.mocked(fs.readFileSync).mockReturnValue(mockYaml);
            MappingService.prototype.getCardMapping = vi.fn().mockReturnValue({ suits: { '0': { name: 'S1' } } } as any);
            const result = deckService.getCards('en');
            expect(result).toBeInstanceOf(Map);
        });
    }, 10000);

    describe('getCardDataForEditionVersionLang', () => {
        let deckService: DeckService;

        const robustMockYaml = `
suits:
  - id: suit1
    name: First Suit
    cards:
      - id: FIRST-CARD
        value: A
        desc: First card
  - id: suit2
    name: Last Suit
    cards:
      - id: LAST-CARD
        value: K
        desc: Last card
  - id: dv
    name: Data Validation
    cards:
      - id: DV-A
        value: A
        desc: Test card description
`;

        const robustMockMapping = {
            suits: {
                '0': { name: 'First Suit' },
                '1': { name: 'Last Suit' },
                '2': { name: 'Data Validation' },
                'suit1': { name: 'First Suit' },
                'suit2': { name: 'Last Suit' },
                'dv': { name: 'Data Validation' }
            }
        };

        beforeEach(() => {
            deckService = new DeckService();
            MappingService.prototype.getCardMapping = vi.fn().mockReturnValue(robustMockMapping as any);
            // Ensure readFileSync returns our data
            vi.mocked(fs.readFileSync).mockImplementation((pathArgs: any) => {
                const pathStr = String(pathArgs).toLowerCase();
                if (pathStr.includes('.yaml') || pathStr.includes('.yml')) return robustMockYaml;
                return '---\n---\nMocked Content';
            });
        });

        it('should return empty map if card file does not exist', () => {
            vi.mocked(FileSystemHelper.hasFile).mockReturnValue(false);
            const result = deckService.getCardDataForEditionVersionLang('webapp', '2.2', 'en');
            expect(result.size).toBe(0);
        });

        it('should load and parse card data correctly', () => {
            const result = deckService.getCardDataForEditionVersionLang('webapp', '2.2', 'en');
            expect(result.size).toBe(3);
            expect(result.get('DV-A')).toBeDefined();
        });

        it('should use English directory if language directory does not exist', () => {
            vi.mocked(FileSystemHelper.hasDir).mockReturnValueOnce(false).mockReturnValueOnce(true);
            const result = deckService.getCardDataForEditionVersionLang('webapp', '2.2', 'es');
            expect(result.size).toBe(3);
        });

        it('should handle navigation for first card', () => {
            const result = deckService.getCardDataForEditionVersionLang('webapp', '2.2', 'en');
            expect(result.get('FIRST-CARD')?.prevous).toBe('LAST-CARD');
        });

        it('should handle navigation for last card', () => {
            const result = deckService.getCardDataForEditionVersionLang('webapp', '2.2', 'en');
            expect(result.get('LAST-CARD')?.next).toBe('FIRST-CARD');
        });

        it('should skip card if technical note file is missing', () => {
            vi.mocked(fs.readFileSync).mockImplementation((pathArgs: any) => {
                const pathStr = String(pathArgs).toLowerCase();
                if (pathStr.includes('technical')) throw new Error('File not found');
                if (pathStr.includes('.yaml')) return robustMockYaml;
                return '---\n---\nMocked Content';
            });
            const spy = vi.spyOn(console, 'error').mockImplementation(() => {});
            const result = deckService.getCardDataForEditionVersionLang('webapp', '2.2', 'en');
            expect(result.size).toBe(0);
            expect(spy).toHaveBeenCalled();
            spy.mockRestore();
        });

        it('should skip card if explanation file is missing', () => {
            vi.mocked(fs.readFileSync).mockImplementation((pathArgs: any) => {
                const pathStr = String(pathArgs).toLowerCase();
                if (pathStr.includes('explanation')) throw new Error('File not found');
                if (pathStr.includes('.yaml')) return robustMockYaml;
                return '---\n---\nMocked Content';
            });
            const spy = vi.spyOn(console, 'error').mockImplementation(() => {});
            const result = deckService.getCardDataForEditionVersionLang('webapp', '2.2', 'en');
            expect(result.size).toBe(0);
            expect(spy).toHaveBeenCalled();
            spy.mockRestore();
        });

        it('should cache loaded cards', () => {
            const spy = vi.spyOn(console, 'log').mockImplementation(() => {});
            deckService.getCardDataForEditionVersionLang('webapp', '2.2', 'en');
            expect(spy).toHaveBeenCalledWith(expect.stringContaining('Caching cards'));
            spy.mockRestore();
        });
    }, 10000);

    describe('clear', () => {
        it('should clear the cache', () => {
            DeckService['cache'].push({ lang: 'en', data: new Map(), version: 'v' });
            DeckService.clear();
            expect(DeckService['cache'].length).toBe(0);
        });
    }, 10000);
});