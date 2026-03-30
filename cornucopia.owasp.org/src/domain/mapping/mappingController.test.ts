import { describe, it, expect } from 'vitest';
import { MappingController } from './mappingController';

describe('mappingController: Complete Coverage', () => {
    it('covers all mapping logic and lookups', () => {
        // Empty state
        const emptyController = new MappingController({});
        expect(emptyController.getWebAppCardMappings('C1')).toEqual({});
        expect(emptyController.getMeta()).toEqual({});

        // Populated state
        const fullController = new MappingController({
            suits: { "S1": { cards: { "C1": "Mapped-C1" } } },
            meta: { project: "Cornucopia" }
        });
        
        expect(fullController.getWebAppCardMappings('C1')).toBe('Mapped-C1');
        expect(fullController.getWebAppCardMappings('invalid')).toEqual({});
        expect(fullController.getMeta()).toEqual({ project: "Cornucopia" });
    });
});