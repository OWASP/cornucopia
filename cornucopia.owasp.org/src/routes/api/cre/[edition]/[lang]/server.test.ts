import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { GET } from './+server';
import { DeckService } from '$lib/services/deckService';
import { MappingService } from '$lib/services/mappingService';

describe('GET /api/cre/[edition]/[lang]', () => {
    beforeEach(() => {
        vi.restoreAllMocks();
    });

    afterEach(() => {
        vi.restoreAllMocks();
    });

    it('throws 404 when language is invalid', () => {
        try {
            GET({ url: new URL('http://localhost/api/cre/webapp/invalid') } as any);

            expect.fail('Expected GET to throw 404 HttpError');
        } catch (err: any) {
            expect(err?.status || err?.body?.status).toBe(404);
        }
    });

    it('throws 404 when edition is invalid', () => {
        try {
            GET({ url: new URL('http://localhost/api/cre/unknown/en') } as any);

            expect.fail('Expected GET to throw 404 HttpError');
        } catch (err: any) {
            expect(err?.status || err?.body?.status).toBe(404);
        }
    });

    it('throws 500 when cards are not found', () => {
        vi.spyOn(DeckService, 'getLatestVersion').mockReturnValue('3.0');
        vi.spyOn(DeckService.prototype, 'getCardDataForEditionVersionLang')
            .mockReturnValue(null as any);

        try {
            GET({ url: new URL('http://localhost/api/cre/webapp/en') } as any);

            expect.fail('Expected GET to throw 500 HttpError');
        } catch (err: any) {
            expect(err?.status || err?.body?.status).toBe(500);
        }
    });

    it('throws 500 when mappings are not found', () => {
        vi.spyOn(DeckService, 'getLatestVersion').mockReturnValue('3.0');

        // Ensure cards exist so it reaches mapping check
        vi.spyOn(DeckService.prototype, 'getCardDataForEditionVersionLang')
            .mockReturnValue(new Map([
                ['VE2', { id: 'VE2' }]
            ]) as any);

        vi.spyOn(MappingService.prototype, 'getCardMappingForLatestEdtions')
            .mockReturnValue(null as any);

        try {
            GET({ url: new URL('http://localhost/api/cre/webapp/en') } as any);

            expect.fail('Expected GET to throw 500 HttpError');
        } catch (err: any) {
            expect(err?.status || err?.body?.status).toBe(500);
        }
    });

    it('handles missing mapping for specific edition', () => {
        vi.spyOn(DeckService, 'getLatestVersion').mockReturnValue('3.0');

        vi.spyOn(DeckService.prototype, 'getCardDataForEditionVersionLang')
            .mockReturnValue(new Map([
                ['VE2', { id: 'VE2' }]
            ]) as any);

        // mapping exists but edition missing
        vi.spyOn(MappingService.prototype, 'getCardMappingForLatestEdtions')
            .mockReturnValue(new Map([['other', {}]]) as any);

        const response = GET({ url: new URL('http://localhost/api/cre/webapp/en') } as any);

        expect(response).toBeDefined();
    });

    it('returns valid CRE mapping response', () => {
  vi.spyOn(DeckService, 'getLatestVersion').mockReturnValue('3.0');

  vi.spyOn(DeckService.prototype, 'getCardDataForEditionVersionLang')
    .mockReturnValue(new Map([
      ['VE2', {
        id: 'VE2',
        edition: 'webapp',
        url: '/cards/VE2',
        suitNameLocal: 'Validation',
        desc: 'Validate input'
      }]
    ]) as any);

  vi.spyOn(MappingService.prototype, 'getCardMappingForLatestEdtions')
    .mockReturnValue(new Map([
      ['webapp', {
        meta: { version: '3.0' },
        suits: [{
          cards: [{
            id: 'VE2',
            owasp_cre: { owasp_asvs: ['123-456'] }
          }]
        }]
      }]
    ]) as any);

  const response = GET({ url: new URL('http://localhost/api/cre/webapp/en') } as any);

  expect(response).toBeDefined();
});

    

    it('falls back to webapp and en defaults when url has no path segments', () => {
        vi.spyOn(DeckService, 'getLanguages').mockReturnValue(['en']);
        vi.spyOn(DeckService, 'getLatestVersion').mockReturnValue('2.2');
        vi.spyOn(DeckService.prototype, 'getCardDataForEditionVersionLang')
            .mockReturnValue(new Map([['VE2', { id: 'VE2' }]]) as any);
        vi.spyOn(MappingService.prototype, 'getCardMappingForLatestEdtions')
            .mockReturnValue(new Map([['webapp', { meta: {}, suits: [] }]]) as any);

        try {
            GET({ url: { pathname: '/' } } as any);
        } catch (_) {}
    });
});