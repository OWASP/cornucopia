import {expect, vi, describe, it, beforeEach} from 'vitest';
import { CreController } from '$domain/cre/creController';
import type { Card } from '$domain/card/card';
import { MappingController } from '../mapping/mappingController';

describe('CreController tests', () => {
    let mockDeck: Map<string, Card>;
    let mockMappingController: MappingController;
    let creController: CreController;

    beforeEach(() => {
        mockDeck = new Map<string, Card>();
        
        mockMappingController = {
            getMeta: vi.fn().mockReturnValue({ version: '1.0.0' }),
            getCardMappings: vi.fn().mockReturnValue({
                owasp_cre: {
                    owasp_asvs: ['CRE-001', 'CRE-002']
                }
            })
        } as any;

        creController = new CreController(mockDeck, mockMappingController);
    });

    describe('getCreMapping', () => {
        it('should return empty structure for unknown edition', () => {
            const result = creController.getCreMapping('unknown', 'en');
            
            expect(result).toEqual({
                meta: {},
                standards: []
            });
        });

        it('should return correct meta and standards for webapp edition', () => {
            const mockCard: Card = {
                id: 'card-1',
                edition: 'webapp',
                suitNameLocal: 'Data Validation',
                desc: 'Test card description',
                url: '/cards/webapp/card-1',
                suit: 'DV',
                value: 'A',
                lang: 'en'
            } as unknown as Card;

            mockDeck.set('card-1', mockCard);
            creController = new CreController(mockDeck, mockMappingController);

            const result = creController.getCreMapping('webapp', 'en');

            expect(result.meta).toEqual({
                edition: 'OWASP Cornucopia Website App Edition',
                component: 'cards',
                language: 'en',
                version: '1.0.0'
            });
            expect(result.standards).toHaveLength(1);
        });

        it('should return correct meta and standards for mobileapp edition', () => {
            const mockCard: Card = {
                id: 'card-2',
                edition: 'mobileapp',
                suitNameLocal: 'Authentication',
                desc: 'Mobile card description',
                url: '/cards/mobileapp/card-2',
                suit: 'AT',
                value: 'K',
                lang: 'en'
            } as unknown as Card;

            mockDeck.set('card-2', mockCard);
            creController = new CreController(mockDeck, mockMappingController);

            const result = creController.getCreMapping('mobileapp', 'es');

            expect(result.meta).toEqual({
                edition: 'OWASP Cornucopia Mobile App Edition',
                component: 'cards',
                language: 'es',
                version: '1.0.0'
            });
            expect(result.standards).toHaveLength(1);
        });

        it('should filter cards by edition', () => {
            const webappCard: Card = {
                id: 'card-1',
                edition: 'webapp',
                suitNameLocal: 'Data Validation',
                desc: 'Webapp card',
                url: '/cards/webapp/card-1',
                suit: 'DV',
                value: 'A',
                lang: 'en'
            } as unknown as Card;

            const mobileappCard: Card = {
                id: 'card-2',
                edition: 'mobileapp',
                suitNameLocal: 'Authentication',
                desc: 'Mobile card',
                url: '/cards/mobileapp/card-2',
                suit: 'AT',
                value: 'K',
                lang: 'en'
            } as unknown as Card;

            mockDeck.set('card-1', webappCard);
            mockDeck.set('card-2', mobileappCard);
            creController = new CreController(mockDeck, mockMappingController);

            const result = creController.getCreMapping('webapp', 'en');

            expect(result.standards).toHaveLength(1);
            expect(result.standards[0].sectionID).toBe('card-1');
        });

        it('should handle empty deck', () => {
            const result = creController.getCreMapping('webapp', 'en');

            expect(result.meta).toEqual({
                edition: 'OWASP Cornucopia Website App Edition',
                component: 'cards',
                language: 'en',
                version: '1.0.0'
            });
            expect(result.standards).toHaveLength(0);
        });
    });

    describe('generateDoc', () => {
        it('should generate correct CRE document structure', () => {
            const mockCard: Card = {
                id: 'card-1',
                edition: 'webapp',
                suitNameLocal: 'Data Validation',
                desc: 'Test card description',
                url: '/cards/webapp/card-1',
                suit: 'DV',
                value: 'A',
                lang: 'en'
            } as unknown as Card;

            const result = creController.generateDoc(mockCard);

            expect(result).toEqual({
                doctype: 'Tool',
                id: 'https://cornucopia.owasp.org/cards/webapp/card-1',
                name: 'OWASP Cornucopia Website App Edition',
                section: 'Data Validation',
                description: 'Test card description',
                sectionID: 'card-1',
                hyperlink: 'https://cornucopia.owasp.org/cards/webapp/card-1',
                links: [
                    {
                        document: {
                            doctype: 'CRE',
                            id: 'CRE-001'
                        },
                        ltype: 'Linked To'
                    },
                    {
                        document: {
                            doctype: 'CRE',
                            id: 'CRE-002'
                        },
                        ltype: 'Linked To'
                    }
                ],
                tags: ['Threat modeling', 'Website Application'],
                tooltype: 'Defensive'
            });
        });

        it('should generate correct document for mobileapp edition', () => {
            const mockCard: Card = {
                id: 'card-2',
                edition: 'mobileapp',
                suitNameLocal: 'Authentication',
                desc: 'Mobile card description',
                url: '/cards/mobileapp/card-2',
                suit: 'AT',
                value: 'K',
                lang: 'en'
            } as unknown as Card;

            const result = creController.generateDoc(mockCard);

            expect(result.name).toBe('OWASP Cornucopia Mobile App Edition');
            expect(result.tags).toContain('Mobile Application');
        });

        it('should handle empty CRE mappings', () => {
            mockMappingController.getCardMappings = vi.fn().mockReturnValue({
                owasp_cre: {
                    owasp_asvs: []
                }
            });

            const mockCard: Card = {
                id: 'card-3',
                edition: 'webapp',
                suitNameLocal: 'Cryptography',
                desc: 'Crypto card',
                url: '/cards/webapp/card-3',
                suit: 'CR',
                value: '2',
                lang: 'en'
            } as unknown as Card;

            const result = creController.generateDoc(mockCard);

            expect(result.links).toHaveLength(0);
        });

        it('When CRE is undefined, links should be empty', () => {
            mockMappingController.getCardMappings = vi.fn().mockReturnValue({
                owasp_cre: {}
            });

            const mockCard: Card = {
                id: 'card-4',
                edition: 'webapp',
                suitNameLocal: 'Test',
                desc: 'Test',
                url: '/test',
                suit: 'TS',
                value: '3',
                lang: 'en'
            } as unknown as Card;
            const result = creController.generateDoc(mockCard);
            expect(result.links).toHaveLength(0);
        });

        it('should handle single CRE mapping', () => {
            mockMappingController.getCardMappings = vi.fn().mockReturnValue({
                owasp_cre: {
                    owasp_asvs: ['CRE-SINGLE']
                }
            });

            const mockCard: Card = {
                id: 'card-5',
                edition: 'webapp',
                suitNameLocal: 'Session Management',
                desc: 'Session card',
                url: '/cards/webapp/card-5',
                suit: 'SM',
                value: 'Q',
                lang: 'en'
            } as unknown as Card;

            const result = creController.generateDoc(mockCard);

            expect(result.links).toHaveLength(1);
            expect(result.links[0].document.id).toBe('CRE-SINGLE');
        });

        it('should construct correct URLs', () => {
            const mockCard = {
                id: 'card-6',
                edition: 'webapp',
                suitNameLocal: 'Authorization',
                desc: 'Auth card',
                url: '/cards/webapp/authorization/card-6',
                suit: 'AZ',
                value: 'J',
                lang: 'en'
            } as unknown as Card;

            const result = creController.generateDoc(mockCard);

            expect(result.id).toBe('https://cornucopia.owasp.org/cards/webapp/authorization/card-6');
            expect(result.hyperlink).toBe('https://cornucopia.owasp.org/cards/webapp/authorization/card-6');
        });
    });

    describe('getEditionName', () => {
        it('should return correct name for webapp edition', () => {
            const result = CreController.getEditionName('webapp');
            expect(result).toBe('OWASP Cornucopia Website App Edition');
        });

        it('should return correct name for mobileapp edition', () => {
            const result = CreController.getEditionName('mobileapp');
            expect(result).toBe('OWASP Cornucopia Mobile App Edition');
        });

        it('should return the edition string itself for unknown edition', () => {
            const result = CreController.getEditionName('unknown-edition');
            expect(result).toBe('unknown-edition');
        });

        it('should handle empty string', () => {
            const result = CreController.getEditionName('');
            expect(result).toBe('');
        });
    });

    describe('Edge cases', () => {
        it('should handle getMeta returning undefined', () => {
            mockMappingController.getMeta = vi.fn().mockReturnValue(undefined);
            creController = new CreController(mockDeck, mockMappingController);

            const result = creController.getCreMapping('webapp', 'en');

            expect(result.meta.version).toBeUndefined();
        });

        it('should handle multiple cards with same edition', () => {
            const card1: Card = {
                id: 'card-1',
                edition: 'webapp',
                suitNameLocal: 'Suite 1',
                desc: 'Card 1',
                url: '/card1',
                suit: 'S1',
                value: 'A',
                lang: 'en'
            } as unknown as Card;

            const card2: Card = {
                id: 'card-2',
                edition: 'webapp',
                suitNameLocal: 'Suite 2',
                desc: 'Card 2',
                url: '/card2',
                suit: 'S2',
                value: 'K',
                lang: 'en'
            } as unknown as Card;

            mockDeck.set('card-1', card1);
            mockDeck.set('card-2', card2);
            creController = new CreController(mockDeck, mockMappingController);

            const result = creController.getCreMapping('webapp', 'en');

            expect(result.standards).toHaveLength(2);
        });
    });
});