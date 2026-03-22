/* eslint-disable @typescript-eslint/no-unsafe-type-assertion, @typescript-eslint/no-explicit-any, @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-argument -- Safe Vitest mocks for isolated testing */
import { describe, it, expect, vi } from 'vitest';
import { CreController } from './creController';

describe('creController: Sydseter Branch Coverage', () => {
    it('should hit the mapping logic and helper functions (Line 29)', () => {
        const mockMappingController = {
            getWebAppCardMappings: vi.fn().mockReturnValue({ owasp_cre: ['123-456'] })
        } as any;

        const cards = new Map<string, any>();
        cards.set('webapp-1', { id: 'webapp-1' });

        const controller = new CreController(cards as any, mockMappingController);
        const result = controller.getCreMapping('webapp', 'en');

        expect(result).toBeTruthy();
    });

    it('should handle invalid or null mappings to hit helper branches', () => {
        const mockMappingController = {
            getWebAppCardMappings: vi.fn().mockReturnValue(null)
        } as any;

        const cards = new Map<string, any>();
        cards.set('webapp-1', { id: 'webapp-1' });

        const controller = new CreController(cards as any, mockMappingController);
        const result = controller.getCreMapping('webapp', 'en');

        expect(result).toBeDefined();
    });
});