import { expect, describe, it, vi, afterEach } from 'vitest';
import fs from 'fs';
import { CardImagesService } from './cardImagesService';

describe('CardImagesService tests', () => {

    afterEach(() => {
        vi.restoreAllMocks();
        CardImagesService.clear();
    });

    it("should return card image data for eop.", () => {
        const service = new CardImagesService();
        const cards = service.getCardImages('eop', '5.0');
        expect(cards).toBeDefined();
        expect(Object.keys(cards as object)).toHaveLength(78);
        expect(cards?.SP2).toEqual({ image: '/images/eop-cards/spoofing-2.png' });
    });

    it('should handle missing card images file gracefully', () => {
        const service = new CardImagesService();
        expect(service.getCardImages('invalid-edition', '0.0')).toBeUndefined();
    });

    it('should return cached card images on repeated calls', () => {
        const service = new CardImagesService();
        const first = service.getCardImages('eop', '5.0');
        const second = service.getCardImages('eop', '5.0');
        // uses reference equality to confirm the second call returns the cached object
        expect(second).toBe(first);
    });

    it('should handle a card images file that fails to parse', () => {
        vi.spyOn(console, 'error').mockImplementation(() => undefined);
        vi.spyOn(fs, 'readFileSync').mockImplementation(() => {
            throw new Error('boom');
        });

        const service = new CardImagesService();
        expect(service.getCardImages('eop', '5.0')).toBeUndefined();
    });
});
