import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { GET } from './+server';
import { DeckService } from '$lib/services/deckService';
import { MappingService } from '$lib/services/mappingService';

describe('GET /api/mapping/[edition]/[version]', () => {
    beforeEach(() => {
        vi.restoreAllMocks();
    });

    afterEach(() => {
        vi.restoreAllMocks();
    });

    it('returns mapping data for a valid edition and version', async () => {
        vi.spyOn(DeckService, 'hasEdition').mockReturnValue(true);
        vi.spyOn(DeckService, 'hasVersion').mockReturnValue(true);
        vi.spyOn(MappingService.prototype, 'getCardMapping').mockReturnValue({
            meta: { edition: 'webapp', component: 'mappings', language: 'ALL', version: '3.0' },
            cards: { VE2: { id: 'VE2' } }
        });
        const response = await GET({ params: { edition: 'webapp', version: '3.0' } } as unknown);
        expect(response.status).toBe(200);
        expect(response.headers.get('content-type')).toContain('application/json');
        const body = await response.json();
        expect(body.meta.version).toBe('3.0');
        expect(body.cards.VE2.id).toBe('VE2');
    });

    it('transforms suits-based mapping into cards map response', async () => {
        vi.spyOn(DeckService, 'hasEdition').mockReturnValue(true);
        vi.spyOn(DeckService, 'hasVersion').mockReturnValue(true);
        vi.spyOn(MappingService.prototype, 'getCardMapping').mockReturnValue({
            meta: { edition: 'webapp', component: 'mappings', language: 'ALL', version: '3.0' },
            suits: [{ cards: [{ id: 'VE2', value: '2' }, { id: 'VE3', value: '3' }] }]
        } as unknown);
        const response = await GET({ params: { edition: 'webapp', version: '3.0' } } as unknown);
        expect(response.status).toBe(200);
        const body = await response.json();
        expect(body.meta.version).toBe('3.0');
        expect(body.cards.VE2.id).toBe('VE2');
        expect(body.cards.VE3.id).toBe('VE3');
        expect(body.suits).toBeUndefined();
    });

    it('skips invalid suits and duplicate or invalid cards while transforming suits', async () => {
        vi.spyOn(DeckService, 'hasEdition').mockReturnValue(true);
        vi.spyOn(DeckService, 'hasVersion').mockReturnValue(true);
        vi.spyOn(MappingService.prototype, 'getCardMapping').mockReturnValue({
            suits: [null, {}, { cards: [null, { id: '' }, { id: 'VE2', value: '2' }, { id: 'VE2', value: 'duplicate' }] }]
        } as unknown);
        const response = await GET({ params: { edition: 'webapp', version: '3.0' } } as unknown);
        expect(response.status).toBe(200);
        const body = await response.json();
        expect(body.meta).toBeUndefined();
        expect(body.cards).toEqual({ VE2: { id: 'VE2', value: '2' } });
    });

    it('throws 404 when edition is invalid', () => {
        vi.spyOn(DeckService, 'hasEdition').mockReturnValue(false);
        vi.spyOn(DeckService, 'getLatestEditions').mockReturnValue(['webapp', 'mobileapp']);
        try {
            GET({ params: { edition: 'unknown', version: '3.0' } } as unknown);
            expect.fail('Expected GET to throw 404 HttpError');
        } catch (err: unknown) {
            expect(err.status).toBe(404);
            expect(err.body.message).toBe('Edition not found. Only: webapp, mobileapp are supported.');
        }
    });

    it('throws 404 when version is invalid for a valid edition', () => {
        vi.spyOn(DeckService, 'hasEdition').mockReturnValue(true);
        vi.spyOn(DeckService, 'hasVersion').mockReturnValue(false);
        vi.spyOn(DeckService, 'getVersions').mockReturnValue(['2.2', '3.0']);
        try {
            GET({ params: { edition: 'webapp', version: '1.0' } } as unknown);
            expect.fail('Expected GET to throw 404 HttpError');
        } catch (err: unknown) {
            expect(err.status).toBe(404);
            expect(err.body.message).toBe('Version not found for edition webapp. Only: 2.2, 3.0 are supported.');
        }
    });

    it('throws 500 when mapping data is not found', () => {
        vi.spyOn(DeckService, 'hasEdition').mockReturnValue(true);
        vi.spyOn(DeckService, 'hasVersion').mockReturnValue(true);
        vi.spyOn(MappingService.prototype, 'getCardMapping').mockReturnValue(undefined as unknown);
        try {
            GET({ params: { edition: 'webapp', version: '3.0' } } as unknown);
            expect.fail('Expected GET to throw 500 HttpError');
        } catch (err: unknown) {
            expect(err.status).toBe(500);
            expect(err.body.message).toBe('No mapping data found.');
        }
    });

    it('throws 500 when mapping data is null', () => {
        vi.spyOn(DeckService, 'hasEdition').mockReturnValue(true);
        vi.spyOn(DeckService, 'hasVersion').mockReturnValue(true);
        vi.spyOn(MappingService.prototype, 'getCardMapping').mockReturnValue(null as unknown);
        try {
            GET({ params: { edition: 'webapp', version: '3.0' } } as unknown);
            expect.fail('Expected GET to throw 500 HttpError');
        } catch (err: unknown) {
            expect(err.status).toBe(500);
        }
    });
});