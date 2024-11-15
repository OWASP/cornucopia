import fm from "front-matter"
import fs from 'fs'
import yaml from "js-yaml";
import type { Card } from "../../domain/card/card";

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
        const cards : Card[] = [];
        for (let i in DeckService.decks) {
            let deck = DeckService.decks[i];
            const requestOptions = {
                method: "GET",
                keepalive: true,
            };
            const response = this.request('GET', `${DeckService.repoUrl}${DeckService.getEdition(deck.edition)}-cards-${deck.version}-${DeckService.getLanguage(deck.edition, lang)}.yaml`);
            if (response.statusCode !== 200) {
                console.error('Request error in deckService. status: ' + response.statusCode + ' , message: ' + response.getBody())
            }
            const data : any = yaml.load(response.getBody().toString());
            const base = `data/cards/${deck.edition}-cards-${DeckService.getVersion(deck.edition)}/`;
            
            for (let suit in data['suits']) {
                let suitObject: any = data['suits'][suit];
                for(let card in suitObject['cards']) {
                    let cardObject = suitObject['cards'][card];
                    cardObject.id = cardObject['id'].replace("COM", "CM");
                    cardObject.suitName = suitObject['name'];
                    cardObject.suitId = suitObject['id'];
                    cardObject.name = `${cardObject.suitName} (${cardObject.id})`;
                    cardObject.suit = cardObject.suitName.replaceAll(' ', '-').toLocaleLowerCase();
                    cardObject.url = `/${cardObject.suit}/${cardObject.id}`;
                    cardObject.githubUrl = `` + cardObject.suit + '/' + cardObject.id;
                    let path : string = `./${base}${cardObject.githubUrl}/technical-note.md`;  // '/explanation.md';
                    let file = fs.readFileSync(path, 'utf8');
                    let parsed = fm(file);
                    cardObject.summary = parsed.body;
                    cards.push(cardObject);
                }
            }
            let file = fs.readFileSync(`./${base}about/CORNUCOPIA/technical-note.md`, 'utf8');
            let parsed = fm(file);

            let explanation = {
                id: 'CORNUCOPIA',
                value: 'Explanation',
                suitId: 'EX',
                name: 'Explanation',
                suitName: 'Instructions',
                suit: 'about',
                url: '/about/CORNUCOPIA',
                githubUrl: `${base}about/CORNUCOPIA`,
                desc: 'OWASP Cornucopia is a mechanism in the form of a card game to assist software development teams identify security requirements in Agile, conventional and formal development processes. It is language, platform and technology-agnostic.',
                summary: parsed.body
            } as Card;
            cards.push(explanation);
        }
        
        DeckService.cache.push({deck: `${DeckService.getEdition(edition)}-${DeckService.getLanguage(edition, lang)}`, data: cards});
        return cards;
    }

    public static clear(): void
    {
        DeckService.cache = [];
        DeckService.mappings = [];
    }
}