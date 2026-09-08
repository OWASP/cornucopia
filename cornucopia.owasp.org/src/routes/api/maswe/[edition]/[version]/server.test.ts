import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { GET } from './+server';
import { DeckService } from '$lib/services/deckService';
import { MasweService } from '$lib/services/masweService';

describe('GET /api/maswe/[edition]/[version]', () => {
    beforeEach(() => {
        vi.restoreAllMocks();
    });

    afterEach(() => {
        vi.restoreAllMocks();
    });

    it('returns MASWE mapping data for a valid edition and version', async () => {
        vi.spyOn(DeckService, 'hasEdition').mockReturnValue(true);
        vi.spyOn(DeckService, 'hasVersion').mockReturnValue(true);
        vi.spyOn(MasweService, 'getMasweData').mockReturnValue({
            meta: { edition: 'mobileapp', component: 'maswe', language: 'ALL', version: '2.0' },
            '0001': { owasp_mastg: ['0207'] }
        });

        const response = await GET({ params: { edition: 'mobileapp', version: '2.0' } } as unknown);

        expect(response.status).toBe(200);
        expect(response.headers.get('content-type')).toContain('application/json');
        expect(await response.json()).toEqual({
            meta: { edition: 'mobileapp', component: 'maswe', language: 'ALL', version: '2.0' },
            '0001': { owasp_mastg: ['0207'] }
        });
    });

    it('throws 404 when edition is invalid', () => {
        vi.spyOn(DeckService, 'hasEdition').mockReturnValue(false);
        vi.spyOn(DeckService, 'getLatestEditions').mockReturnValue(['webapp', 'mobileapp']);

        expect(() => GET({ params: { edition: 'unknown', version: '2.0' } } as unknown)).toThrow();
    });

    it('throws 404 when version is invalid', () => {
        vi.spyOn(DeckService, 'hasEdition').mockReturnValue(true);
        vi.spyOn(DeckService, 'hasVersion').mockReturnValue(false);
        vi.spyOn(DeckService, 'getVersions').mockReturnValue(['1.1', '2.0']);

        expect(() => GET({ params: { edition: 'mobileapp', version: '1.0' } } as unknown)).toThrow();
    });

    it('throws 500 when MASWE data is empty', () => {
        vi.spyOn(DeckService, 'hasEdition').mockReturnValue(true);
        vi.spyOn(DeckService, 'hasVersion').mockReturnValue(true);
        vi.spyOn(MasweService, 'getMasweData').mockReturnValue({});

        expect(() => GET({ params: { edition: 'mobileapp', version: '2.0' } } as unknown)).toThrow();
    });
});
