import { expect, describe, it, vi, afterEach } from 'vitest';
import { DeckService } from './deckService';
import { MappingService } from './mappingService';

describe('MappingService tests', () => {

    afterEach(() => {
        vi.restoreAllMocks();
        MappingService.clear();
    });

    it("should return card mapping data.", async () => {
        expect((new MappingService()).getCardMappingForLatestEdtions()).toBeDefined();
        MappingService.clear();
        expect((new MappingService()).getCardMappingForAllVersions().get('webapp-2.2')).toBeDefined();
        expect((new MappingService()).getCardMappingForAllVersions().get('webapp-3.0')).toBeDefined();
        expect((new MappingService()).getCardMappingForAllVersions().get('mobileapp-1.1')).toBeDefined();
    }); 

    it('should handle missing mapping file gracefully', () => {
        const service = new MappingService();
        expect(service.getCardMapping('invalid-edition', '0.0')).toBeUndefined();
    });

    it('should return empty or default mapping for unknown data', () => {
        const service = new MappingService();
        expect(service.getCardMapping('webapp', 'invalid-version')).toBeUndefined();
    });

    it('should skip missing mapping files', () => {
        const service = new MappingService();
        const decks = DeckService.getDecks();

        service.getCardMappingForAllVersions();

        vi.spyOn(console, 'error').mockImplementation(() => undefined);
        vi.spyOn(DeckService, 'getDecks').mockReturnValue([
            ...decks,
            { edition: 'missing', version: '9.9', lang: ['en'] }
        ]);

        expect(service.getCardMappingForAllVersions().get('missing-9.9')).toBeUndefined();
    });
});