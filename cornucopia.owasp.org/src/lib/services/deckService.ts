import fm from "front-matter"
import fs from 'fs'
import * as yaml from "js-yaml";
import type { Card } from "$domain/card/card";
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import path from "path";
import type { Deck } from "$domain/deck/deck";
import { MappingService } from "$lib/services/mappingService";
import { DeckConfigService } from "$lib/services/deckConfigService";
const __dirname = path.resolve(path.dirname(''));
export class DeckService {

    constructor() {
    }
    private static path: string = '/../source/';
    private static cache: object[] = [];
    private static _decks: Deck[] | undefined;
    private static _latests: Deck[] | undefined;

    private static discoverLanguages(edition: string, version: string): string[] {
        const dir = `${__dirname}${DeckService.path}`;
        if (!FileSystemHelper.hasDir(dir)) return [];

        const prefix = `${edition}-cards-${version}-`;
        const draftLanguages = new Set(DeckConfigService.getDraftLanguages(edition, version));

        return FileSystemHelper.getFiles(dir)
            .filter((file) => file.startsWith(prefix) && file.endsWith('.yaml'))
            .map((file) => file.slice(prefix.length, -'.yaml'.length))
            .filter((lang) => !draftLanguages.has(lang));
    }

    private static buildDecks(): Deck[] {
        const decks: Deck[] = [];
        DeckConfigService.getDeckConfigs().forEach((config) => {
            config.versions.forEach((versionConfig) => {
                const lang = DeckService.discoverLanguages(config.edition, versionConfig.version);
                if (lang.length > 0) {
                    decks.push({ edition: config.edition, version: versionConfig.version, lang });
                }
            });
        });
        return decks;
    }

    private static buildLatests(decks: Deck[]): Deck[] {
        const latests: Deck[] = [];
        DeckConfigService.getDeckConfigs().forEach((config) => {
            const versions = config.versions.map((v) => v.version);
            const latestVersion = versions[versions.length - 1];
            const deck = decks.find((d) => d.edition === config.edition && d.version === latestVersion);
            if (deck) latests.push(deck);
        });
        return latests;
    }

    private static getAllDecks(): Deck[] {
        if (!DeckService._decks) {
            DeckService._decks = DeckService.buildDecks();
        }
        return DeckService._decks;
    }

    private static getLatestDecks(): Deck[] {
        if (!DeckService._latests) {
            DeckService._latests = DeckService.buildLatests(DeckService.getAllDecks());
        }
        return DeckService._latests;
    }

    public static hasEdition(edition: string): boolean {
        return DeckService.getAllDecks().find((deck) => deck.edition == edition) != undefined;
    }

    public static hasVersion(edition: string, version: string): boolean {
        return DeckService.getAllDecks().find((deck) => (deck.edition == edition && deck.version == version)) != undefined;
    }

    public static hasLanguage(edition: string, lang: string): boolean {
        return DeckService.getAllDecks().find((deck) => (deck.edition == edition && deck.lang.includes(lang))) != undefined;
    }

    public static getDecks(): Deck[] {
        return DeckService.getAllDecks();
    }

    public static getLatestVersion(edition: string): string {
        return DeckService.getLatestDecks().find((deck) => deck.edition == edition)?.version || '3.0';
    }

    public static getLatestEditions(): string[] {
        return DeckService.getLatestDecks().map((deck) => deck.edition);
    }

    public static getLanguages(edition: string): string[] {
        const languages: string[] = DeckService.getAllDecks().filter((deck) => deck.edition == edition).flatMap((deck) => deck.lang);
        return languages.length !== 0 ? languages : ['en'];
    }
    public static getLanguagesForEditionVersion(edition: string, version: string): string[] {
        const deck = DeckService.getAllDecks().find((d) => d.edition === edition && d.version === version);
        return deck?.lang ?? [];
    }
    public static getVersions(edition: string): string[] {
        return DeckService.getAllDecks().filter((deck) => deck.edition == edition).flatMap((deck) => deck.version);
    }

    public getCards(lang: string): Map<string, Card> {
        return DeckService.cache.find((deck) => deck?.lang == lang && deck?.version == 'latest')?.data || this.getCardData(lang);
    }


  private getCardData(lang: string)
{
    let cards = new Map<string, Card>;
    const decks = DeckService.getLatestDecks();

    for (const i in decks) {
        cards = new Map([
            ...this.getCardDataForEditionVersionLang(decks[i].edition, decks[i].version, lang),
            ...cards
        ]);
    }

    DeckService.cache.push({lang: lang, data: cards, version: 'latest'});
    return cards; 
} 
    public getCardDataForEditionVersionLang(edition: string, version: string, lang: string) {

        const cards = new Map<string, Card>;

        const cardFile = `${__dirname}${DeckService.path}${edition}-cards-${version}-${lang}.yaml`;

        if (!FileSystemHelper.hasFile(cardFile)) {
            console.warn(`Card file not found: ${cardFile}`);
            return cards;
        }

        const yamlData = fs.readFileSync(cardFile, 'utf8');
        const data = yaml.load(yamlData, { schema: yaml.FAILSAFE_SCHEMA });
        let base = `data/cards/${edition}-cards-${version}-${lang}/`;

        if (!FileSystemHelper.hasDir(base)) {
            base = `data/cards/${edition}-cards-${version}-en/`;
        }

        const mapping = (new MappingService()).getCardMapping(edition, version);
        const editionDisplayName = DeckConfigService.getDisplayName(edition);
        const isExternalEdition = DeckConfigService.isExternal(edition);

        for (const suit in data['suits']) {
            const suitObject: Record<string, unknown> = data['suits'][suit];
            const suitName: string = mapping['suits'][suit]['name'];
            for (const card in suitObject['cards']) {
                const cardObject = suitObject['cards'][card];
                cardObject.edition = edition;
                cardObject.editionName = editionDisplayName;
                cardObject.version = version;
                cardObject.language = lang;
                cardObject.suitName = suitName;
                cardObject.suitNameLocal = suitObject['name'];
                cardObject.suitId = suitObject['id'];
                cardObject.name = `${cardObject.suitName} (${cardObject.id})`;
                cardObject.suit = cardObject.suitName.replaceAll(' ', '-').toLocaleLowerCase();

                if (!isExternalEdition) {
                    cardObject.url = `/edition/${edition}/${cardObject.id}/${version}/${lang}`;
                }

                const cardFolderPath = cardObject.suit + '/' + cardObject.id;
                if (!isExternalEdition) {
                    cardObject.githubUrl = base + cardFolderPath + '/explanation.md';
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

                cards.set(cardObject.id, cardObject);

                if (!isExternalEdition) {
                    const path: string = `./${base}${cardFolderPath}/technical-note.md`;
                    try {
                        cardObject.concept = fm(fs.readFileSync(path, 'utf8')).body;
                    } catch {
                        console.warn(`Error: Missing technical-note for ${cardObject.id || 'unknown'} at ${path}`);
                        continue;
                    }

                    const explanationPath = `./${base}${cardFolderPath}/explanation.md`;
                    try {
                        cardObject.summary = fm(fs.readFileSync(explanationPath, 'utf8')).body;
                    } catch {
                        console.warn(`Error: Missing explanation for ${cardObject.id || 'unknown'} at ${explanationPath}`);
                        continue;
                    }
                }

                cards.set(cardObject.id, cardObject);
            }
        }

        console.log(`Caching cards for ${edition} ${version} ${lang} - total cards: ${cards.size}`);

        DeckService.cache.push({ edition: edition, version: version, lang: lang, data: cards });
        return cards;
    }

    public static clear(): void {
        DeckService.cache = [];
        DeckService._decks = undefined;
        DeckService._latests = undefined;
    }
}
