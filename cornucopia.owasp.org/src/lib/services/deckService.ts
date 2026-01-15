import fm from "front-matter"
import fs from 'fs'
import yaml from "js-yaml";
import type { Card } from "$domain/card/card";
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import path from "path";
const __dirname = path.resolve(path.dirname(''));
export class DeckService {

    constructor() {
    }
    private static path: string = '/../source/';
    private static cache: object[] = [];
    private static mappings: object[] = [];

    private static readonly latests = [
        {lang: ['en'], edition: 'mobileapp', version: '1.1'}, 
        {lang: ['en', 'es', 'fr', 'nl', 'no_nb', 'pt_br', 'pt_pt', 'ru', 'it'], edition: 'webapp', version: '2.2'}
    ];
    private static readonly decks = [
        {edition: 'mobileapp', version: '1.1', lang: ['en']},
        {edition: 'webapp', version: '2.2', lang: ['en', 'es', 'fr', 'nl', 'no_nb', 'pt_br', 'pt_pt', 'ru', 'it']},
        {edition: 'webapp', version: '3.0', lang: ['en']}];

    public static hasEdition(edition: string): boolean
    {
        return DeckService.decks.find((deck) => deck.edition == edition) != undefined;
    }

    public static hasVersion(edition: string, version: string): boolean
    {
        return DeckService.decks.find((deck) => (deck.edition == edition && deck.version == version)) != undefined;
    }

    public static hasLanguage(edition: string, lang: string): boolean
    {
        return DeckService.decks.find((deck) => (deck.edition == edition && deck.lang.includes(lang))) != undefined;
    }

    public static getEditions(): string[]
    {
        return DeckService.decks.map((deck) => deck.edition);
    }

    public static getLatestLanguages(edition: string): string[]
    {
        return DeckService.latests.find((deck) => deck.edition == edition)?.lang || ['en'];
    }

    public static getLatestVersion(edition: string): string
    {
        return DeckService.latests.find((deck) => deck.edition == edition)?.version || '2.2';
    }

    public static getVersion(edition: string): string
    {
        return DeckService.decks.find((deck: { edition: string; }) => deck.edition == edition)?.version || '2.2';
    }

    public static getEdition(edition: string): string
    {
        return DeckService.decks.find((deck: { edition: string; }) => deck.edition == edition)?.edition || 'webapp';
    }

    private static getLanguage(edition: string, lang: string) : string
    {
        return DeckService.latests.find((deck) => (deck.edition == edition && deck.lang.includes(lang))) ? lang : 'en';
    }

    public static getLanguages(edition: string) : string[]
    {
        let languages : string[] = DeckService.decks.filter((deck) => deck.edition == edition).flatMap((deck) => deck.lang);
        return languages.length !== 0 ? languages : ['en'];
    }
    public static getVersions(edition: string) : string[]
    {
        return DeckService.decks.filter((deck) => deck.edition == edition).flatMap((deck) => deck.version);
    }

    private getLatestsCardMappingData(edition: string)
    {
        const yamlData = fs.readFileSync(`${__dirname}${DeckService.path}${DeckService.getEdition(edition)}-mappings-${DeckService.getVersion(edition)}.yaml`, 'utf8');
        let data = yaml.load(yamlData);
        DeckService.mappings.push({edition: DeckService.getEdition(edition), version: 'latests', data: data});
        return data;
    }

    private getCardMappingDataAllVersions()
    {
        const decksList = DeckService.decks;
        decksList.forEach((deck) => {
            const yamlData = fs.readFileSync(`${__dirname}${DeckService.path}${DeckService.getEdition(deck.edition)}-mappings-${deck.version}.yaml`, 'utf8');
            let data = yaml.load(yamlData);
            DeckService.mappings.push({edition: deck.edition, version: deck.version, data: data});
        });
        
        return DeckService.mappings;
    }

    public getCardMapping() : Map<string, any>
    {
        const decks = new Map<string, any>();
        const editions = DeckService.latests;
        editions.forEach((deck) => {
            decks.set(
                deck.edition, DeckService.mappings.find((mapping) => mapping?.version == 'latests' && mapping?.edition == deck.edition)?.data || this.getLatestsCardMappingData(deck.edition)
            );

            
        });
        return decks;
    }

    public getCardMappingForAllVersions() : Map<string, any>
    {
        const decks = new Map<string, any>();
        const editions = DeckService.decks;
        editions.forEach((deck) => {
            decks.set(
                `${deck.edition}-${deck.version}`, DeckService.mappings.find((mapping) => mapping?.version == deck.version && mapping?.edition == deck.edition)?.data || this.getCardMappingDataAllVersions()
            );
            
        });
        return decks;
    }

    public getCards(lang: string): Map<string, Card>
    {
        return DeckService.cache.find((deck) => deck?.lang == lang && deck?.version == 'latest')?.data || this.getCardData(lang);
    }

    public getCardsForAllVersionsAndLanguages() : Map<string, any>
    {
        const decks = new Map<string, any>(); 
        const decksList = DeckService.decks;
        decksList.forEach((edition) => {
            edition.lang.forEach((language) => {
                if (decks.has(`${edition.version}-${language}`)) {
                    decks.set(
                        `${edition.version}-${language}`, decks.get(`${edition.version}-${language}`).merge(
                            this.getCardDataForEditionVersionLang(edition.edition, edition.version, language)));
                } else {
                    decks.set(`${edition.version}-${language}`, this.getCardDataForEditionVersionLang(edition.edition, edition.version, language));
                }
            });

        });
        return decks;
    }

    private getCardData(lang: string)
    {
        const cards = new Map<string, Card>;
        const decks = DeckService.latests;
        for (let i in decks) {
            let deck = decks[i];
            let yamlData = fs.readFileSync(`${__dirname}${DeckService.path}${DeckService.getEdition(deck.edition)}-cards-${deck.version}-${DeckService.getLanguage(deck.edition, lang)}.yaml`, 'utf8');
            console.log("Loading cards from file: " + `${__dirname}${DeckService.path}${DeckService.getEdition(deck.edition)}-cards-${deck.version}-${DeckService.getLanguage(deck.edition, lang)}.yaml`);
            let data = yaml.load(yamlData);
            let mapping = this.getCardMapping().get(deck.edition);
            let base = `data/cards/${deck.edition}-cards-${DeckService.getVersion(deck.edition)}-${lang}/`;

            if(!FileSystemHelper.hasDir(base)) {
                return cards;
            }
            
            for (let suit in data['suits']) {
                let suitObject: any = data['suits'][suit];
                let suitName: string = mapping['suits'][suit] != undefined ? mapping['suits'][suit]['name'] : 'WILD CARD';
                for(let card in suitObject['cards']) {
                    
                    let cardObject = suitObject['cards'][card];
                    cardObject.id = cardObject['id'];
                    cardObject.edition = deck.edition;
                    cardObject.version = deck.version;
                    cardObject.language = lang;
                    cardObject.suitName = suitName;
                    cardObject.suitNameLocal = suitObject['name'];
                    cardObject.suitId = suitObject['id'];
                    cardObject.name = `${cardObject.suitName} (${cardObject.id})`;
                    cardObject.suit = cardObject.suitName.replaceAll(' ', '-').toLocaleLowerCase();
                    cardObject.url = `/card/${deck.edition}/${cardObject.id}/${deck.version}/${lang}`;
                    cardObject.githubUrl = `` + cardObject.suit + '/' + cardObject.id;
                    let path : string = `./${base}${cardObject.githubUrl}/technical-note.md`;  // '/explanation.md';
                    let file: string;
                    try {
                        file = fs.readFileSync(path, 'utf8');
                    } catch (e) {
                        console.error(`Error reading file at path: ${path}`, e);
                        continue;
                    }
                    let parsed = fm(file);
                    cardObject.concept = parsed.body;
                    try {
                        cardObject.summary = fm(fs.readFileSync(`./${base}${cardObject.githubUrl}/explanation.md`, 'utf8')).body;
                    } catch (e) {
                        console.error(`Error reading file at path: ./${base}${cardObject.githubUrl}/explanation.md`, e);
                        continue;
                    }
                    
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
                    cardObject.prevous = cardObject.prevous;
                    cardObject.next = cardObject.next;
                    
                    cards.set(cardObject.id, cardObject);
                }
            }
        }
        DeckService.cache.push({lang: lang, data: cards, version: 'latest'});
        return cards;
    }

    public getCardsForAllLanguages() : Map<string, any>
    {
        const languages: string[] = DeckService.latests[1].lang;
        let decks = new Map<string, any>();

        const editions = DeckService.latests;
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

    
    public getCardDataForEditionVersionLang(edition:string, version: string, lang: string)
    {
        const cards = new Map<string, Card>;

        let cardFile = `${__dirname}${DeckService.path}${edition}-cards-${version}-${lang}.yaml`;

        if(!FileSystemHelper.hasFile(cardFile)) {
            return cards;
        }

        let yamlData = fs.readFileSync(cardFile, 'utf8');
        let data = yaml.load(yamlData);
        let mapping = this.getCardMapping().get(edition);
        let base = `data/cards/${edition}-cards-${version}-${lang}/`;

        if(!FileSystemHelper.hasDir(base)) {
            base = `data/cards/${edition}-cards-${version}-en/`;
        }

        for (let suit in data['suits']) {
            let suitObject: any = data['suits'][suit];
            let suitName: string = mapping['suits'][suit] != undefined ? mapping['suits'][suit]['name'] : 'WILD CARD';
            for(let card in suitObject['cards']) {
                let cardObject = suitObject['cards'][card];
                cardObject.id = cardObject['id'];
                cardObject.edition = edition;
                cardObject.version = version;
                cardObject.language = lang;
                cardObject.suitName = suitName;
                cardObject.suitNameLocal = suitObject['name'];
                cardObject.suitId = suitObject['id'];
                cardObject.name = `${cardObject.suitName} (${cardObject.id})`;
                cardObject.suit = cardObject.suitName.replaceAll(' ', '-').toLocaleLowerCase();
                cardObject.url = `/card/${edition}/${cardObject.id}/${version}/${lang}`;
                cardObject.githubUrl = `` + cardObject.suit + '/' + cardObject.id;
                let path : string = `./${base}${cardObject.githubUrl}/technical-note.md`;  // '/explanation.md';
                let file = fs.readFileSync(path, 'utf8');
                let parsed = fm(file);
                cardObject.concept = parsed.body;
                cardObject.summary = fm(fs.readFileSync(`./${base}${cardObject.githubUrl}/explanation.md`, 'utf8')).body;

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
                cardObject.prevous = cardObject.prevous;
                cardObject.next = cardObject.next;
                
                cards.set(cardObject.id, cardObject);
            }
        }

        console.log(`Caching cards for ${edition} ${version} ${lang} - total cards: ${cards.size}`);

        DeckService.cache.push({edition: edition, version: version, lang: lang, data: cards});
        return cards;
    }

    public static clear(): void
    {
        DeckService.cache = [];
        DeckService.mappings = [];
    }
}
