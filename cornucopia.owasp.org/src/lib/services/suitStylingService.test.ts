import { expect, describe, it, vi, afterEach } from 'vitest';
import fs from 'fs';
import { SuitStylingService } from './suitStylingService';

describe('SuitStylingService tests', () => {

    afterEach(() => {
        vi.restoreAllMocks();
        SuitStylingService.clear();
    });

    it("should return suit styling data for eop.", () => {
        const service = new SuitStylingService();
        const suits = service.getSuitStyling('eop', '5.0');
        expect(suits).toBeDefined();
        expect(Object.keys(suits as object)).toHaveLength(6);
        expect(suits?.spoofing).toEqual({ tab: '#861a10', watermark: '#bdbcbc', royal: '#c60751' });
    });

    it('should handle missing styling file', () => {
        const service = new SuitStylingService();
        expect(service.getSuitStyling('invalid-edition', '0.0')).toBeUndefined();
    });

    it('should return cached suit styling on repeated calls', () => {
        const service = new SuitStylingService();
        const first = service.getSuitStyling('eop', '5.0');
        const second = service.getSuitStyling('eop', '5.0');
        // uses reference equality to confirm the second call returns the cached object
        expect(second).toBe(first);
    });

    it('should handle a styling file that fails to parse', () => {
        vi.spyOn(console, 'error').mockImplementation(() => undefined);
        vi.spyOn(fs, 'readFileSync').mockImplementation(() => {
            throw new Error('boom');
        });

        const service = new SuitStylingService();
        expect(service.getSuitStyling('eop', '5.0')).toBeUndefined();
    });
});
