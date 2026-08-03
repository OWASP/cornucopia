import { expect, describe, it, afterEach } from 'vitest';
import { CardImagesService } from './cardImagesService';

describe('CardImagesService tests', () => {

    afterEach(() => {
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
});
