import { expect, describe, it, afterEach } from 'vitest';
import { CardImagesService } from './cardImagesService';

describe('CardImagesService tests', () => {

    afterEach(() => {
        CardImagesService.clear();
    });

    it("should return card image data for eop.", async () => {
        const service = new CardImagesService();
        const cards = service.getCardImages('eop', '5.0');
        expect(cards).toBeDefined();
        expect(Object.keys(cards as object)).toHaveLength(78);
        expect(cards?.SP2).toEqual({ image: '/images/eop-cards/spoofing-2.png' });
    });

    it('should mark the known opaque cards', () => {
        const cards = (new CardImagesService()).getCardImages('eop', '5.0');
        expect(cards?.TA2.opaque).toBeTruthy();
        expect(cards?.EP2.opaque).toBeTruthy();
        expect(cards?.EP3.opaque).toBeTruthy();
        expect(cards?.EP4.opaque).toBeTruthy();
        expect(cards?.SP2.opaque).toBeUndefined();
    });

    it('should handle missing card images file gracefully', () => {
        const service = new CardImagesService();
        expect(service.getCardImages('invalid-edition', '0.0')).toBeUndefined();
    });
});
