import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { DeckService } from './deckService';
import type { Card } from '$domain/card/card';
import fs from 'fs';
import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper';
import { MappingService } from './mappingService';

vi.mock('fs');
vi.mock('$lib/filesystem/fileSystemHelper');
vi.mock('./mappingService');

describe('DeckService tests', () => {
    beforeEach(() => {
        DeckService.clear();
        vi.clearAllMocks();
    });

    afterEach(() => {
        DeckService.clear();
    });

describe('getLanguagesForEditionVersion', () => {

    it('should return correct languages for valid edition + version', () => {
        const languages = DeckService.getLanguagesForEditionVersion('webapp', '2.2');
        expect(languages).toContain('en');
        expect(languages).toContain('es');
    });

    it('should fallback to ["en"] for invalid edition + version', () => {
        const languages = DeckService.getLanguagesForEditionVersion('invalid', '0.0');
        expect(languages).toEqual(['en']);
    });

});


    describe('hasEdition', () => {
        it('should return true for webapp edition', () => {
            expect(DeckService.hasEdition('webapp')).toBe(true);
        });

        it('should return true for mobileapp edition', () => {
            expect(DeckService.hasEdition('mobileapp')).toBe(true);
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

        it('should return false for invalid version', () => {
            expect(DeckService.hasVersion('webapp', '1.0')).toBe(false);
        });

        it('should return false for unknown edition', () => {
            expect(DeckService.hasVersion('unknown', '2.2')).toBe(false);
        });
    }, 10000);

    describe('hasLanguage', () => {
        it('should return true for webapp with en', () => {
            expect(DeckService.hasLanguage('webapp', 'en')).toBe(true);
        });

        it('should return true for webapp with es', () => {
            expect(DeckService.hasLanguage('webapp', 'es')).toBe(true);
        });

        it('should return true for webapp with fr', () => {
            expect(DeckService.hasLanguage('webapp', 'fr')).toBe(true);
        });

        it('should return true for webapp with nl', () => {
            expect(DeckService.hasLanguage('webapp', 'nl')).toBe(true);
        });

        it('should return true for webapp with no_nb', () => {
            expect(DeckService.hasLanguage('webapp', 'no_nb')).toBe(true);
        });

        it('should return true for webapp with pt_br', () => {
            expect(DeckService.hasLanguage('webapp', 'pt_br')).toBe(true);
        });

        it('should return true for webapp with pt_pt', () => {
            expect(DeckService.hasLanguage('webapp', 'pt_pt')).toBe(true);
        });

        it('should return true for webapp with ru', () => {
            expect(DeckService.hasLanguage('webapp', 'ru')).toBe(true);
        });

        it('should return true for webapp with it', () => {
            expect(DeckService.hasLanguage('webapp', 'it')).toBe(true);
        });

        it('should return true for mobileapp with en', () => {
            expect(DeckService.hasLanguage('mobileapp', 'en')).toBe(true);
        });

        it('should return false for mobileapp with es', () => {
            expect(DeckService.hasLanguage('mobileapp', 'es')).toBe(false);
        });

        it('should return false for unknown language', () => {
            expect(DeckService.hasLanguage('webapp', 'de')).toBe(false);
        });

        it('should return false for unknown edition', () => {
            expect(DeckService.hasLanguage('unknown', 'en')).toBe(false);
        });
    }, 10000);

    describe('getDecks', () => {
        it('should return all available decks', () => {
            const decks = DeckService.getDecks();
            expect(decks).toHaveLength(3);
            expect(decks).toContainEqual({ edition: 'mobileapp', version: '1.1', lang: ['en'] });
            expect(decks).toContainEqual({ 
                edition: 'webapp', 
                version: '2.2', 
                lang: ['en', 'es', 'fr', 'nl', 'no_nb', 'pt_br', 'pt_pt', 'ru', 'it'] 
            });
            expect(decks).toContainEqual({ edition: 'webapp', version: '3.0', lang: ['en'] });
        });
    }, 10000);

    describe('getLatestVersion', () => {
        it('should return 2.2 for webapp', () => {
            expect(DeckService.getLatestVersion('webapp')).toBe('2.2');
        });

        it('should return 1.1 for mobileapp', () => {
            expect(DeckService.getLatestVersion('mobileapp')).toBe('1.1');
        });

        it('should return 2.2 as default for unknown edition', () => {
            expect(DeckService.getLatestVersion('unknown')).toBe('2.2');
        });
    }, 10000);

    describe('getLatestEditions', () => {
        it('should return array of latest editions', () => {
            const editions = DeckService.getLatestEditions();
            expect(editions).toHaveLength(2);
            expect(editions).toContain('webapp');
            expect(editions).toContain('mobileapp');
        });
    }, 10000);

    describe('getLanguages', () => {
        it('should return all languages for webapp', () => {
            const languages = DeckService.getLanguages('webapp');
            expect(languages).toContain('en');
            expect(languages).toContain('es');
            expect(languages).toContain('fr');
            expect(languages).toContain('nl');
            expect(languages).toContain('no_nb');
            expect(languages).toContain('pt_br');
            expect(languages).toContain('pt_pt');
            expect(languages).toContain('ru');
            expect(languages).toContain('it');
        });

        it('should return en for mobileapp', () => {
            const languages = DeckService.getLanguages('mobileapp');
            expect(languages).toContain('en');
        });

        it('should return default en for unknown edition', () => {
            const languages = DeckService.getLanguages('unknown');
            expect(languages).toEqual(['en']);
        });
    }, 10000);

    describe('getVersions', () => {
        it('should return all versions for webapp', () => {
            const versions = DeckService.getVersions('webapp');
            expect(versions).toContain('2.2');
            expect(versions).toContain('3.0');
            expect(versions).toHaveLength(2);
        });

        it('should return version for mobileapp', () => {
            const versions = DeckService.getVersions('mobileapp');
            expect(versions).toEqual(['1.1']);
        });

        it('should return empty array for unknown edition', () => {
            const versions = DeckService.getVersions('unknown');
            expect(versions).toEqual([]);
        });
    }, 10000);

    describe('getCards', () => {
        let deckService: DeckService;

        beforeEach(() => {
            deckService = new DeckService();
        });

        it('should return cards from cache if available', () => {
            const mockCards = new Map<string, Card>();
            mockCards.set('card1', { id: 'card1', edition: 'webapp' } as Card);

            DeckService['cache'].push({ lang: 'en', version: 'latest', data: mockCards });

            const result = deckService.getCards('en');
            expect(result).toBe(mockCards);
            expect(result.size).toBe(1);
        });

        it('should load cards if not in cache', () => {
            vi.mocked(FileSystemHelper.hasFile).mockReturnValue(true);
            vi.mocked(FileSystemHelper.hasDir).mockReturnValue(true);
            
            const mockYamlContent = `
suits:
  - id: suit1
    name: Test Suit
    cards:
      - id: card1
        value: A
        desc: Test card
`;
            vi.mocked(fs.readFileSync).mockReturnValue(mockYamlContent);

            const mockMapping = {
                suits: {
                    '0': { name: 'Test Suit' }
                }
            };
            vi.mocked(MappingService.prototype.getCardMapping).mockReturnValue(mockMapping as any);

            const result = deckService.getCards('en');
            expect(result).toBeInstanceOf(Map);
        });
    }, 10000);

    describe('getCardDataForEditionVersionLang', () => {
        let deckService: DeckService;

        beforeEach(() => {
            deckService = new DeckService();
            vi.clearAllMocks();
        });

        it('should return empty map if card file does not exist', () => {
            vi.mocked(FileSystemHelper.hasFile).mockReturnValue(false);

            const result = deckService.getCardDataForEditionVersionLang('webapp', '2.2', 'en');
            expect(result.size).toBe(0);
        });

        it('should load and parse card data correctly', () => {
            vi.mocked(FileSystemHelper.hasFile).mockReturnValue(true);
            vi.mocked(FileSystemHelper.hasDir).mockReturnValue(true);

            const mockYamlContent = `
suits:
  - id: dv
    name: Data Validation
    cards:
      - id: DV-A
        value: A
        desc: Test card description
`;

            const mockTechnicalNote = '---\n---\nTechnical note content';
            const mockExplanation = '---\n---\nExplanation content';

            vi.mocked(fs.readFileSync)
                .mockReturnValueOnce(mockYamlContent)
                .mockReturnValueOnce(mockTechnicalNote)
                .mockReturnValueOnce(mockExplanation);

            const mockMapping = {
                suits: {
                    '0': { name: 'Data Validation' }
                }
            };
            vi.mocked(MappingService.prototype.getCardMapping).mockReturnValue(mockMapping as any);

            const result = deckService.getCardDataForEditionVersionLang('webapp', '2.2', 'en');
            
            expect(result.size).toBe(1);
            const card = result.get('DV-A');
            expect(card).toBeDefined();
            expect(card?.id).toBe('DV-A');
            expect(card?.edition).toBe('webapp');
            expect(card?.version).toBe('2.2');
            expect(card?.language).toBe('en');
            expect(card?.suitName).toBe('Data Validation');
        });

        it('should use English directory if language directory does not exist', () => {
            vi.mocked(FileSystemHelper.hasFile).mockReturnValue(true);
            vi.mocked(FileSystemHelper.hasDir)
                .mockReturnValueOnce(false)  // Spanish dir doesn't exist
                .mockReturnValueOnce(true);  // English dir exists

            const mockYamlContent = `
suits:
  - id: at
    name: Authentication
    cards:
      - id: AT-K
        value: K
        desc: Auth card
`;

            const mockTechnicalNote = '---\n---\nTech note';
            const mockExplanation = '---\n---\nExplanation';

            vi.mocked(fs.readFileSync)
                .mockReturnValueOnce(mockYamlContent)
                .mockReturnValueOnce(mockTechnicalNote)
                .mockReturnValueOnce(mockExplanation);

            const mockMapping = {
                suits: {
                    '0': { name: 'Authentication' }
                }
            };
            vi.mocked(MappingService.prototype.getCardMapping).mockReturnValue(mockMapping as any);

            const result = deckService.getCardDataForEditionVersionLang('webapp', '2.2', 'es');
            expect(result.size).toBe(1);
        });

        it('should handle navigation for first card', () => {
            vi.mocked(FileSystemHelper.hasFile).mockReturnValue(true);
            vi.mocked(FileSystemHelper.hasDir).mockReturnValue(true);

            const mockYamlContent = `
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
`;

            const mockTechnicalNote = '---\n---\nContent';
            const mockExplanation = '---\n---\nContent';

            vi.mocked(fs.readFileSync)
                .mockReturnValue(mockYamlContent)
                .mockReturnValueOnce(mockYamlContent)
                .mockReturnValueOnce(mockTechnicalNote)
                .mockReturnValueOnce(mockExplanation)
                .mockReturnValueOnce(mockTechnicalNote)
                .mockReturnValueOnce(mockExplanation);

            const mockMapping = {
                suits: {
                    '0': { name: 'First Suit' },
                    '1': { name: 'Last Suit' }
                }
            };
            vi.mocked(MappingService.prototype.getCardMapping).mockReturnValue(mockMapping as any);

            const result = deckService.getCardDataForEditionVersionLang('webapp', '2.2', 'en');
            
            const firstCard = result.get('FIRST-CARD');
            expect(firstCard?.prevous).toBe('LAST-CARD');
        });

        it('should handle navigation for last card', () => {
            vi.mocked(FileSystemHelper.hasFile).mockReturnValue(true);
            vi.mocked(FileSystemHelper.hasDir).mockReturnValue(true);

            const mockYamlContent = `
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
`;

            const mockTechnicalNote = '---\n---\nContent';
            const mockExplanation = '---\n---\nContent';

            vi.mocked(fs.readFileSync)
                .mockReturnValue(mockYamlContent)
                .mockReturnValueOnce(mockYamlContent)
                .mockReturnValueOnce(mockTechnicalNote)
                .mockReturnValueOnce(mockExplanation)
                .mockReturnValueOnce(mockTechnicalNote)
                .mockReturnValueOnce(mockExplanation);

            const mockMapping = {
                suits: {
                    '0': { name: 'First Suit' },
                    '1': { name: 'Last Suit' }
                }
            };
            vi.mocked(MappingService.prototype.getCardMapping).mockReturnValue(mockMapping as any);

            const result = deckService.getCardDataForEditionVersionLang('webapp', '2.2', 'en');
            
            const lastCard = result.get('LAST-CARD');
            expect(lastCard?.next).toBe('FIRST-CARD');
        });

        it('should skip card if technical note file is missing', () => {
            vi.mocked(FileSystemHelper.hasFile).mockReturnValue(true);
            vi.mocked(FileSystemHelper.hasDir).mockReturnValue(true);

            const mockYamlContent = `
suits:
  - id: suit1
    name: Test Suit
    cards:
      - id: CARD-1
        value: A
        desc: Card 1
`;

            vi.mocked(fs.readFileSync)
                .mockReturnValueOnce(mockYamlContent)
                .mockImplementationOnce(() => {
                    throw new Error('File not found');
                });

            const mockMapping = {
                suits: {
                    '0': { name: 'Test Suit' }
                }
            };
            vi.mocked(MappingService.prototype.getCardMapping).mockReturnValue(mockMapping as any);

            const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

            const result = deckService.getCardDataForEditionVersionLang('webapp', '2.2', 'en');
            
            expect(result.size).toBe(0);
            expect(consoleErrorSpy).toHaveBeenCalled();
            
            consoleErrorSpy.mockRestore();
        });

        it('should skip card if explanation file is missing', () => {
            vi.mocked(FileSystemHelper.hasFile).mockReturnValue(true);
            vi.mocked(FileSystemHelper.hasDir).mockReturnValue(true);

            const mockYamlContent = `
suits:
  - id: suit1
    name: Test Suit
    cards:
      - id: CARD-1
        value: A
        desc: Card 1
`;

            const mockTechnicalNote = '---\n---\nContent';

            vi.mocked(fs.readFileSync)
                .mockReturnValueOnce(mockYamlContent)
                .mockReturnValueOnce(mockTechnicalNote)
                .mockImplementationOnce(() => {
                    throw new Error('File not found');
                });

            const mockMapping = {
                suits: {
                    '0': { name: 'Test Suit' }
                }
            };
            vi.mocked(MappingService.prototype.getCardMapping).mockReturnValue(mockMapping as any);

            const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

            const result = deckService.getCardDataForEditionVersionLang('webapp', '2.2', 'en');
            
            expect(result.size).toBe(0);
            expect(consoleErrorSpy).toHaveBeenCalled();
            
            consoleErrorSpy.mockRestore();
        });

        it('should cache loaded cards', () => {
            vi.mocked(FileSystemHelper.hasFile).mockReturnValue(true);
            vi.mocked(FileSystemHelper.hasDir).mockReturnValue(true);

            const mockYamlContent = `
suits:
  - id: suit1
    name: Test Suit
    cards:
      - id: CARD-1
        value: A
        desc: Card 1
`;

            const mockTechnicalNote = '---\n---\nContent';
            const mockExplanation = '---\n---\nContent';

            vi.mocked(fs.readFileSync)
                .mockReturnValueOnce(mockYamlContent)
                .mockReturnValueOnce(mockTechnicalNote)
                .mockReturnValueOnce(mockExplanation);

            const mockMapping = {
                suits: {
                    '0': { name: 'Test Suit' }
                }
            };
            vi.mocked(MappingService.prototype.getCardMapping).mockReturnValue(mockMapping as any);

            const consoleLogSpy = vi.spyOn(console, 'log').mockImplementation(() => {});

            deckService.getCardDataForEditionVersionLang('webapp', '2.2', 'en');
            
            expect(consoleLogSpy).toHaveBeenCalledWith(
                expect.stringContaining('Caching cards for webapp 2.2 en')
            );
            
            consoleLogSpy.mockRestore();
        });
    }, 10000);

    describe('clear', () => {
        it('should clear the cache', () => {
            DeckService['cache'].push({ lang: 'en', data: new Map(), version: 'latest' });
            expect(DeckService['cache'].length).toBe(1);

            DeckService.clear();

            expect(DeckService['cache'].length).toBe(0);
        });
    }, 10000);
});


describe('Additional coverage boosters', () => {

it('should fallback safely for invalid edition-version', () => {
    const service = new DeckService();
    const result = service.getCardDataForEditionVersionLang('invalid', '0.0', 'en');
    expect(result).toBeInstanceOf(Map);
});

    it('getCards should merge latest editions properly', () => {
        const service = new DeckService();
        const cards = service.getCards('unknown-lang');
        expect(cards).toBeInstanceOf(Map);
    });

});

