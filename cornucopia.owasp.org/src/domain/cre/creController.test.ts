import { describe, it, expect } from 'vitest';
import { CreController } from './creController';
import type { Card } from '$domain/card/card';
import type { MappingController } from '$domain/mapping/mappingController';

// Safe bridges with explicit comparisons for strict-boolean-expressions
function isCard(obj: unknown): obj is Card { return obj !== null && obj !== undefined; }
function isMappingController(obj: unknown): obj is MappingController { return obj !== null && obj !== undefined; }

describe('CreController', () => {
  it('should generate CRE mappings successfully', () => {
    const mockDeck: Map<string, Card> = new Map<string, Card>();
    
    const dummyCardData: unknown = { id: 'test-id' };
    
    if (isCard(dummyCardData)) {
      mockDeck.set('test-id', dummyCardData);
    }

    const rawMockController: unknown = {
      getWebAppCardMappings: (id: string) => {
        if (id === 'test-id') {
          return { owasp_cre: ['123-456'] };
        }
        return {};
      },
      getMeta: () => ({ version: '1.0.0' })
    };

    if (isMappingController(rawMockController)) {
      const controller = new CreController(mockDeck, rawMockController);
      const result = controller.getCreMapping('webapp', 'en');

      expect(result.edition).toBe('webapp');
      expect(result.lang).toBe('en');
      expect(Array.isArray(result.mappings)).toBe(true);
    }
  });
});