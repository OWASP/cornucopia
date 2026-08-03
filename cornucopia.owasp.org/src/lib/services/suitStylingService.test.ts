import { expect, describe, it, afterEach } from 'vitest';
import { SuitStylingService } from './suitStylingService';

describe('SuitStylingService tests', () => {

    afterEach(() => {
        SuitStylingService.clear();
    });

    it("should return suit styling data for eop.", async () => {
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
});
