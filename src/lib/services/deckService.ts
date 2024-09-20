import yaml from "js-yaml";
import request from "sync-request";
import { type Response } from 'then-request';

export class DeckService {
    private request: any;
    constructor(request: any) {
        this.request = request;
    }
    private static repoUrl: string = 'https://raw.githubusercontent.com/OWASP/cornucopia/master/source/';
    private static cache: object[] = [];
    private static mappings: object[] = [];

    private static languages = [
        {lang: ['en'], edition: 'mobileapp'}, 
        {lang: ['en', 'es', 'fr', 'nl', 'no_nb', 'pt_br'], edition: 'webapp'}
    ];
    private static decks = [{edition: 'mobileapp', version: '1.00'}, {edition: 'webapp', version: '2.00'}];

    private static getVersion(edition: string): string
    {
        return DeckService.decks.find((deck) => deck.edition == edition)?.version || '2.00';
    }

    private static getEdition(edition: string): string
    {
        return DeckService.decks.find((deck) => deck.edition == edition)?.edition || 'webapp';
    }

    private static getLanguage(edition: string, lang: string) : string
    {
        return DeckService.languages.find((deck) => (deck.edition == edition && deck.lang.includes(lang))) ? lang : 'en';
    }

    private getCardMappingData(edition: string)
    {
        const requestOptions = {
            method: "GET",
            keepalive: true,
        };
        const response = this.request('GET', `${DeckService.repoUrl}${DeckService.getEdition(edition)}-mappings-${DeckService.getVersion(edition)}.yaml`);
        if (response.statusCode !== 200) {
            console.error('Request error in deckService. status: ' + response.statusCode + ' , message: ' + response.getBody())
        }
        const data = yaml.load(response.getBody().toString());
        DeckService.mappings.push({edition: DeckService.getEdition(edition), data: data});
        return data;
    }

    public getCardMapping(edition: string)
    {
        return DeckService.mappings.find((mapping) => mapping?.edition == DeckService.getEdition(edition))?.data || this.getCardMappingData(edition);
    }

    public getCards(edition: string, lang: string)
    {
        return DeckService.cache.find((mapping) => mapping?.deck == `${DeckService.getEdition(edition)}-${DeckService.getLanguage(edition, lang)}`)?.data || this.getCardData(edition, lang);
    }

    private getCardData(edition: string, lang: string)
    {
        const requestOptions = {
            method: "GET",
            keepalive: true,
        };
        const response = this.request('GET', `${DeckService.repoUrl}${DeckService.getEdition(edition)}-cards-${DeckService.getVersion(edition)}-${DeckService.getLanguage(edition, lang)}.yaml`);
        if (response.statusCode !== 200) {
            console.error('Request error in deckService. status: ' + response.statusCode + ' , message: ' + response.getBody())
        }
        const data = yaml.load(response.getBody().toString());
        DeckService.cache.push({deck: `${DeckService.getEdition(edition)}-${DeckService.getLanguage(edition, lang)}`, data: data});
        return data;
    }

    public static clear(): void
    {
        DeckService.cache = [];
        DeckService.mappings = [];
    }
}