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
        let response = this.request('GET', `${DeckService.repoUrl}${DeckService.getEdition(edition)}-mappings-${DeckService.getVersion(edition)}.yaml`);
        if (response.statusCode !== 200) {
            console.error('Request error in deckService. status: ' + response.statusCode + ' , message: ' + response.getBody())
        }
        let data = yaml.load(response.getBody().toString());
        DeckService.mappings.push({edition: DeckService.getEdition(edition), data: data});
        return data;
    }

    public getCardMapping(edition: string)
    {
        return DeckService.mappings.find((mapping) => mapping?.edition == DeckService.getEdition(edition))?.data || this.getCardMappingData(edition);
    }

    public getCards(lang: string): Map<string, Card>
    {
        return DeckService.cache.find((mapping) => mapping?.lang == lang)?.data || this.getCardData(lang);
    }

    public getCardsForAllLanguages() : Map<string, any>
    {
        const languages: string[] = DeckService.languages[1].lang;
        let decks = new Map<string, any>();

        const editions = DeckService.languages;
        editions.forEach((edition, index) => {
            languages.forEach((language, lang) => {
                if (!editions[index].lang.includes(language)) language = 'en';
                decks.set(
                    language, this.getCards(language)
                );

            });
            
        });
        return decks;
    }

    private getCardData(lang: string)
    {
        const cards = new Map<string, Card>;
        for (let i in DeckService.decks) {
            let deck = DeckService.decks[i];
            const requestOptions = {
                method: "GET",
                keepalive: true,
            };
            let response = this.request('GET', `${DeckService.repoUrl}${DeckService.getEdition(deck.edition)}-cards-${deck.version}-${DeckService.getLanguage(deck.edition, lang)}.yaml`);
            if (response.statusCode !== 200) {
                console.error('Request error in deckService. status: ' + response.statusCode + ' , message: ' + response.getBody())
            }
            let data : any = yaml.load(response.getBody().toString());
            let mapping = this.getCardMapping(deck.edition);
            let base = `data/cards/${deck.edition}-cards-${DeckService.getVersion(deck.edition)}/`;
            
            for (let suit in data['suits']) {
                let suitObject: any = data['suits'][suit];
                let suitName: string = mapping['suits'][suit] != undefined ? mapping['suits'][suit]['name'] : 'WILD CARD';
                for(let card in suitObject['cards']) {
                    let cardObject = suitObject['cards'][card];
                    cardObject.id = cardObject['id'].replace("COM", "CM");
                    cardObject.suitName = suitName;
                    cardObject.suitId = suitObject['id'];
                    cardObject.name = `${cardObject.suitName} (${cardObject.id})`;
                    cardObject.suit = cardObject.suitName.replaceAll(' ', '-').toLocaleLowerCase();
                    cardObject.url = `/${cardObject.suit}/${cardObject.id}`;
                    cardObject.githubUrl = `` + cardObject.suit + '/' + cardObject.id;
                    let path : string = `./${base}${cardObject.githubUrl}/technical-note.md`;  // '/explanation.md';
                    let file = fs.readFileSync(path, 'utf8');
                    let parsed = fm(file);
                    cardObject.summary = parsed.body;

                    if (+card == 0 && +suit == 0) {
                        cardObject.prevous = data['suits'][(+data['suits'].length-1)]['cards'][+data['suits'][(+data['suits'].length-1)]['cards'].length-1]['id'];
                    } else if (Number(card) == 0) {
                        cardObject.prevous = data['suits'][+suit-1]['cards'][+data['suits'][+suit-1]['cards'].length-1]['id'];
                    } else {
                        cardObject.prevous = suitObject['cards'][+card-1]['id'];
                    }

                    if (suitObject['cards'].length == +card+1 && data['suits'].length == +suit+1) {
                        cardObject.next = data['suits'][0]['cards'][0]['id'];
                    } else if (suitObject['cards'].length == +card+1) {
                        cardObject.next = data['suits'][+suit+1]['cards'][0]['id'];
                    } else {
                        cardObject.next = suitObject['cards'][+card+1]['id'];
                    }
                    
                    cards.set(cardObject.id, cardObject);
                }
            }
        }
        DeckService.cache.push({lang: lang, data: cards});
        return cards;
    }

    public static clear(): void
    {
        DeckService.cache = [];
        DeckService.mappings = [];
    }
}