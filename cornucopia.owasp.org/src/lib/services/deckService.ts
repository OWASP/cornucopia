import fm from "front-matter"
import fs from 'fs'
import yaml from "js-yaml";
import type { Card } from "$domain/card/card";
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import path from "path";
import type { Deck } from "$domain/deck/deck";
import { MappingService } from "$lib/services/mappingService";
const __dirname = path.resolve(path.dirname(''));
export class DeckService {

    constructor() {
    }
    private static path: string = '/../source/';
    private static cache: object[] = [];

    private static readonly latests: Deck[] = [
        { lang: ['en'], edition: 'mobileapp', version: '1.1' },
        { lang: ['en', 'es', 'fr', 'nl', 'no_nb', 'pt_br', 'pt_pt', 'ru', 'it'], edition: 'webapp', version: '2.2' }
    ];
    private static readonly decks: Deck[] = [
        { edition: 'mobileapp', version: '1.1', lang: ['en'] },
        { edition: 'webapp', version: '2.2', lang: ['en', 'es', 'fr', 'nl', 'no_nb', 'pt_br', 'pt_pt', 'ru', 'it'] },
        { edition: 'webapp', version: '3.0', lang: ['en', 'ru'] }];

    public static hasEdition(edition: string): boolean {
        return DeckService.decks.find((deck) => deck.edition == edition) != undefined;
    }

    public static hasVersion(edition: string, version: string): boolean {
        return DeckService.decks.find((deck) => (deck.edition == edition && deck.version == version)) != undefined;
    }

    public static hasLanguage(edition: string, lang: string): boolean {
        return DeckService.decks.find((deck) => (deck.edition == edition && deck.lang.includes(lang))) != undefined;
    }

    public static getDecks(): Deck[] {
        return DeckService.decks;
    }

    public static getLatestVersion(edition: string): string {
        return DeckService.latests.find((deck) => deck.edition == edition)?.version || '2.2';
    }

    public static getLatestEditions(): string[] {
        return DeckService.latests.map((deck) => deck.edition);
    }

    public static getLanguages(edition: string): string[] {
        let languages: string[] = DeckService.decks.filter((deck) => deck.edition == edition).flatMap((deck) => deck.lang);
        return languages.length !== 0 ? languages : ['en'];
    }
    public static getVersions(edition: string): string[] {
        return DeckService.decks.filter((deck) => deck.edition == edition).flatMap((deck) => deck.version);
    }

    public getCards(lang: string): Map<string, Card> {
        return DeckService.cache.find((deck) => deck?.lang == lang && deck?.version == 'latest')?.data || this.getCardData(lang);
    }

    private getCardData(lang: string) {
        let cards = new Map<string, Card>;
        const decks = DeckService.latests;
        for (let i in decks) {
            cards = new Map([...this.getCardDataForEditionVersionLang(decks[i].edition, decks[i].version, lang), ...cards]);
            DeckService.cache.push({ lang: lang, data: cards, version: 'latest' });
        }
        return cards;
    }

    public getCardDataForEditionVersionLang(edition: string, version: string, lang: string) {
        const cards = new Map<string, Card>;

        let cardFile = `${__dirname}${DeckService.path}${edition}-cards-${version}-${lang}.yaml`;

        if (!FileSystemHelper.hasFile(cardFile)) {
            return cards;
        }

        let yamlData = fs.readFileSync(cardFile, 'utf8');
        let data = yaml.load(yamlData);
        let base = `data/cards/${edition}-cards-${version}-${lang}/`;

        if (!FileSystemHelper.hasDir(base)) {
            base = `data/cards/${edition}-cards-${version}-en/`;
        }

        let mapping = (new MappingService()).getCardMapping(edition, version);

        for (let suit in data['suits']) {
            let suitObject: any = data['suits'][suit];
            let suitName: string = mapping['suits'][suit]['name'];
            for (let card in suitObject['cards']) {
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
                cardObject.url = `/edition/${edition}/${cardObject.id}/${version}/${lang}`;
                let cardFolderPath = cardObject.suit + '/' + cardObject.id;
                cardObject.githubUrl = base + cardFolderPath + '/explanation.md';

                let path: string = `./${base}${cardFolderPath}/technical-note.md`;  // '/explanation.md';
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
                    cardObject.summary = fm(fs.readFileSync(`./${base}${cardFolderPath}/explanation.md`, 'utf8')).body;
                } catch (e) {
                    console.error(`Error reading file at path: ./${base}${cardFolderPath}/explanation.md`, e);
                    continue;
                }


                if (+card == 0 && +suit == 0) {
                    cardObject.prevous = data['suits'][(+data['suits'].length - 1)]['cards'][+data['suits'][(+data['suits'].length - 1)]['cards'].length - 1]['id'];
                } else if (Number(card) == 0) {
                    cardObject.prevous = data['suits'][+suit - 1]['cards'][+data['suits'][+suit - 1]['cards'].length - 1]['id'];
                } else {
                    cardObject.prevous = suitObject['cards'][+card - 1]['id'];
                }

                if (suitObject['cards'].length == +card + 1 && data['suits'].length == +suit + 1) {
                    cardObject.next = data['suits'][0]['cards'][0]['id'];
                } else if (suitObject['cards'].length == +card + 1) {
                    cardObject.next = data['suits'][+suit + 1]['cards'][0]['id'];
                } else {
                    cardObject.next = suitObject['cards'][+card + 1]['id'];
                }
                cardObject.prevous = cardObject.prevous;
                cardObject.next = cardObject.next;

                cards.set(cardObject.id, cardObject);
            }
        }

        console.log(`Caching cards for ${edition} ${version} ${lang} - total cards: ${cards.size}`);

        DeckService.cache.push({ edition: edition, version: version, lang: lang, data: cards });
        return cards;
    }

    public static clear(): void {
        DeckService.cache = [];
    }
}
