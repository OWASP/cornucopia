import {expect, vi, describe, it} from 'vitest';
import { DeckService } from './deckService';
import { type Response } from 'then-request';
import fs from "fs";

describe('DeckService tests', () => {
    it("should return card mapping data and call the correct url.", async () => {
        const body = fs.readFileSync("data/mock/mapping.yaml", 'utf8');
        const mockResponse = {
            statusCode: 200,
            headers: {},
            body: '',
            url: '',
            isError: () => false,
            getBody: () => body
        } as Response;
        const request = vi.fn(() => mockResponse);
        request.prototype = vi.fn(() => mockResponse);
        vi.doMock('sync-request', async () => {
            await import('sync-request');
            
            return { request };
          });
        expect((new DeckService(request)).getCardMapping('doesntexist')).toBeDefined();
        expect(request).toHaveBeenCalled();
        expect(request).toBeCalledWith('GET', 'https://raw.githubusercontent.com/OWASP/cornucopia/master/source/webapp-mappings-2.00.yaml');
        request.mockClear();
        DeckService.clear();
        expect((new DeckService(request)).getCardMapping('webapp')).toBeDefined();
        expect(request).toHaveBeenCalled();
        expect(request).toBeCalledWith('GET', 'https://raw.githubusercontent.com/OWASP/cornucopia/master/source/webapp-mappings-2.00.yaml');
        request.mockClear();
        DeckService.clear();
        expect((new DeckService(request)).getCardMapping('mobileapp')).toBeDefined();
        expect(request).toHaveBeenCalled();
        expect(request).toBeCalledWith('GET', 'https://raw.githubusercontent.com/OWASP/cornucopia/master/source/mobileapp-mappings-1.00.yaml');
        DeckService.clear();

    });
    it("should return card deck data and call the correct url.", async () => {
        const body = fs.readFileSync("data/mock/cards.yaml", 'utf8');
        const mockResponse = {
            statusCode: 200,
            headers: {},
            body: '',
            url: '',
            isError: () => false,
            getBody: () => body
        } as Response;
        const request = vi.fn(() => mockResponse);
        request.prototype = vi.fn(() => mockResponse);
        vi.doMock('sync-request', async () => {
            await import('sync-request');
            
            return { request };
          });
        request.mockClear();
        DeckService.clear();
        expect((new DeckService(request)).getCards('doesntexist')).toBeDefined();
        expect(request).toHaveBeenCalled();
        expect(request).toBeCalledWith('GET', 'https://raw.githubusercontent.com/OWASP/cornucopia/master/source/webapp-cards-2.00-en.yaml');
        request.mockClear();
        DeckService.clear();
        expect((new DeckService(request)).getCards('doesntexist')).toBeDefined();
        expect(request).toHaveBeenCalled();
        expect(request).toBeCalledWith('GET', 'https://raw.githubusercontent.com/OWASP/cornucopia/master/source/webapp-cards-2.00-en.yaml');
        request.mockClear();
        DeckService.clear();
        expect((new DeckService(request)).getCards('en')).toBeDefined();
        expect(request).toHaveBeenCalled();
        expect(request).toBeCalledWith('GET', 'https://raw.githubusercontent.com/OWASP/cornucopia/master/source/webapp-cards-2.00-en.yaml');
        request.mockClear();
        DeckService.clear();
        expect((new DeckService(request)).getCards('en')).toBeDefined();
        expect(request).toHaveBeenCalled();
        expect(request).toBeCalledWith('GET', 'https://raw.githubusercontent.com/OWASP/cornucopia/master/source/mobileapp-cards-1.00-en.yaml');
        request.mockClear();
        expect((new DeckService(request)).getCards('es')).toBeDefined();
        expect(request).toHaveBeenCalled();
        expect(request).toBeCalledWith('GET', 'https://raw.githubusercontent.com/OWASP/cornucopia/master/source/webapp-cards-2.00-es.yaml');
        request.mockClear();
        expect((new DeckService(request)).getCards('fr')).toBeDefined();
        expect(request).toHaveBeenCalled();
        expect(request).toBeCalledWith('GET', 'https://raw.githubusercontent.com/OWASP/cornucopia/master/source/webapp-cards-2.00-fr.yaml');
        request.mockClear();
        expect((new DeckService(request)).getCards('nl')).toBeDefined();
        expect(request).toHaveBeenCalled();
        expect(request).toBeCalledWith('GET', 'https://raw.githubusercontent.com/OWASP/cornucopia/master/source/webapp-cards-2.00-nl.yaml');
        request.mockClear();
        expect((new DeckService(request)).getCards('no_nb')).toBeDefined();
        expect(request).toHaveBeenCalled();
        expect(request).toBeCalledWith('GET', 'https://raw.githubusercontent.com/OWASP/cornucopia/master/source/webapp-cards-2.00-no_nb.yaml');
        request.mockClear();
        expect((new DeckService(request)).getCards('pt_br')).toBeDefined();
        expect(request).toHaveBeenCalled();
        expect(request).toBeCalledWith('GET', 'https://raw.githubusercontent.com/OWASP/cornucopia/master/source/webapp-cards-2.00-pt_br.yaml');
        request.mockClear();
        DeckService.clear();
    });
});
