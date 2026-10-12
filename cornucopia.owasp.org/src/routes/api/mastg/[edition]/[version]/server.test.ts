import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { GET } from './+server';
import { DeckService } from '$lib/services/deckService';
import { MastgService } from '$lib/services/mastgService';

describe('GET /api/mastg/[edition]/[version]', () => {
    beforeEach(() => {
        vi.restoreAllMocks();
    });

    afterEach(() => {
        vi.restoreAllMocks();
    });

    it('returns MASTG mapping data for a valid edition and version', async () => {
        vi.spyOn(DeckService, 'hasEdition').mockReturnValue(true);
        vi.spyOn(DeckService, 'hasVersion').mockReturnValue(true);
        vi.spyOn(MastgService, 'getMastgData').mockReturnValue({
            meta: { edition: 'mobileapp', component: 'mastg', language: 'ALL', version: '2.0' },
            '0200': { owasp_maswe: ['0002'] }
        });

        const response = await GET({ params: { edition: 'mobileapp', version: '2.0' } } as unknown);

        expect(response.status).toBe(200);
        expect(response.headers.get('content-type')).toContain('application/json');
        expect(await response.json()).toEqual({
            meta: { edition: 'mobileapp', component: 'mastg', language: 'ALL', version: '2.0' },
            '0200': { owasp_maswe: ['0002'] }
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

    it('throws 404 for an edition without MASTG mapping data', () => {
        vi.spyOn(DeckService, 'hasEdition').mockReturnValue(true);
        const getMastgData = vi.spyOn(MastgService, 'getMastgData');

        expect(() => GET({ params: { edition: 'webapp', version: '3.0' } } as unknown)).toThrow();
        expect(getMastgData).not.toHaveBeenCalled();
    });

    it('throws 404 for a version without MASTG mapping data', () => {
        vi.spyOn(DeckService, 'hasEdition').mockReturnValue(true);
        vi.spyOn(DeckService, 'hasVersion').mockReturnValue(true);
        const getMastgData = vi.spyOn(MastgService, 'getMastgData');

        expect(() => GET({ params: { edition: 'mobileapp', version: '1.1' } } as unknown)).toThrow();
        expect(getMastgData).not.toHaveBeenCalled();
    });

    it('throws 500 when MASTG data is empty', () => {
        vi.spyOn(DeckService, 'hasEdition').mockReturnValue(true);
        vi.spyOn(DeckService, 'hasVersion').mockReturnValue(true);
        vi.spyOn(MastgService, 'getMastgData').mockReturnValue({});

        expect(() => GET({ params: { edition: 'mobileapp', version: '2.0' } } as unknown)).toThrow();
    });
});
