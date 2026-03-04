import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { GET } from './+server';
import { DeckService } from '$lib/services/deckService';

describe('GET /api/lang/[edition]/[version]', () => {
    beforeEach(() => {
        vi.restoreAllMocks();
    });

    afterEach(() => {
        vi.restoreAllMocks();
    });

    it('returns languages for a valid edition and version', async () => {
        vi.spyOn(DeckService, 'hasEdition').mockReturnValue(true);
        vi.spyOn(DeckService, 'hasVersion').mockReturnValue(true);
        vi.spyOn(DeckService, 'getLanguagesForEditionVersion').mockReturnValue(['en', 'ru']);

        const response = await GET({
            params: { edition: 'webapp', version: '3.0' }
        } as any);

        expect(response.status).toBe(200);
        expect(response.headers.get('content-type')).toContain('application/json');

        const body = await response.json();
        expect(body).toEqual({
            meta: {
                component: 'cards',
                language: 'all',
                languages: ['en', 'ru'],
                version: '3.0'
            }
        });
    });

    it('throws 404 when edition is invalid', () => {
        vi.spyOn(DeckService, 'hasEdition').mockReturnValue(false);
        vi.spyOn(DeckService, 'getLatestEditions').mockReturnValue(['webapp', 'mobileapp']);

        try {
            GET({
                params: { edition: 'unknown', version: '3.0' }
            } as any);

            expect.fail('Expected GET to throw 404 HttpError');
        } catch (err: any) {
            expect(err.status).toBe(404);
            expect(err.body.message).toBe('Edition not found. Only: webapp, mobileapp are supported.');
        }
    });

    it('throws 404 when version is invalid for a valid edition', () => {
        vi.spyOn(DeckService, 'hasEdition').mockReturnValue(true);
        vi.spyOn(DeckService, 'hasVersion').mockReturnValue(false);
        vi.spyOn(DeckService, 'getVersions').mockReturnValue(['2.2', '3.0']);

        try {
            GET({
                params: { edition: 'webapp', version: '1.0' }
            } as any);

            expect.fail('Expected GET to throw 404 HttpError');
        } catch (err: any) {
            expect(err.status).toBe(404);
            expect(err.body.message).toBe('Version not found for edition webapp. Only: 2.2, 3.0 are supported.');
        }
    });

    it('throws 404 when edition param is missing', () => {
        vi.spyOn(DeckService, 'getLatestEditions').mockReturnValue(['webapp', 'mobileapp']);

        try {
            GET({
                params: { version: '3.0' }
            } as any);

            expect.fail('Expected GET to throw 404 HttpError');
        } catch (err: any) {
            expect(err.status).toBe(404);
            expect(err.body.message).toBe('Edition not found. Only: webapp, mobileapp are supported.');
        }
    });

    it('throws 404 when version param is missing', () => {
        vi.spyOn(DeckService, 'hasEdition').mockReturnValue(true);
        vi.spyOn(DeckService, 'getVersions').mockReturnValue(['2.2', '3.0']);

        try {
            GET({
                params: { edition: 'webapp' }
            } as any);

            expect.fail('Expected GET to throw 404 HttpError');
        } catch (err: any) {
            expect(err.status).toBe(404);
            expect(err.body.message).toBe('Version not found for edition webapp. Only: 2.2, 3.0 are supported.');
        }
    });
});
