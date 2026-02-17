import fm from "front-matter";
import fs from "fs";
import yaml from "js-yaml";
import type { Card } from "$domain/card/card";
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import path from "path";
import type { Deck } from "$domain/deck/deck";
import { MappingService } from "$lib/services/mappingService";

const __dirname = path.resolve(path.dirname(""));

type DeckCacheEntry = {
    edition?: string;
    version: string;
    lang: string;
    data: Map<string, Card>;
};

export class DeckService {

    constructor() {}

    private static path: string = "/../source/";
    private static cache: DeckCacheEntry[] = [];

    private static readonly latests: Deck[] = [
        { lang: ["en"], edition: "mobileapp", version: "1.1" },
        { lang: ["en", "es", "fr", "nl", "no_nb", "pt_br", "pt_pt", "ru", "it"], edition: "webapp", version: "2.2" }
    ];

    private static readonly decks: Deck[] = [
        { edition: "mobileapp", version: "1.1", lang: ["en"] },
        { edition: "webapp", version: "2.2", lang: ["en", "es", "fr", "nl", "no_nb", "pt_br", "pt_pt", "ru", "it"] },
        { edition: "webapp", version: "3.0", lang: ["en"] }
    ];

    public static hasEdition(edition: string): boolean {
        return DeckService.decks.find((deck) => deck.edition === edition) !== undefined;
    }

    public static hasVersion(edition: string, version: string): boolean {
        return DeckService.decks.find(
            (deck) => deck.edition === edition && deck.version === version
        ) !== undefined;
    }

    public static hasLanguage(edition: string, lang: string): boolean {
        return DeckService.decks.find(
            (deck) => deck.edition === edition && deck.lang.includes(lang)
        ) !== undefined;
    }

    public static getDecks(): Deck[] {
        return DeckService.decks;
    }

    public static getLatestVersion(edition: string): string {
        return (
            DeckService.latests.find((deck) => deck.edition === edition)?.version ||
            "2.2"
        );
    }

    public static getLatestEditions(): string[] {
        return DeckService.latests.map((deck) => deck.edition);
    }

    public static getLanguages(edition: string): string[] {
        const languages: string[] = DeckService.decks
            .filter((deck) => deck.edition === edition)
            .flatMap((deck) => deck.lang);

        return languages.length !== 0 ? languages : ["en"];
    }

    public static getLanguagesForEditionVersion(
        edition: string,
        version: string
    ): string[] {
        const deck = DeckService.decks.find(
            (d) => d.edition === edition && d.version === version
        );

        return deck ? deck.lang : ["en"];
    }

    public static getVersions(edition: string): string[] {
        return DeckService.decks
            .filter((deck) => deck.edition === edition)
            .flatMap((deck) => deck.version);
    }

    public getCards(lang: string): Map<string, Card> {
        const cached = DeckService.cache.find(
            (deck) => deck.lang === lang && deck.version === "latest"
        );

        return cached?.data || this.getCardData(lang);
    }

    private getCardData(lang: string): Map<string, Card> {
        let cards = new Map<string, Card>();
        const decks = DeckService.latests;

        for (const deck of decks) {
            cards = new Map([
                ...this.getCardDataForEditionVersionLang(
                    deck.edition,
                    deck.version,
                    lang
                ),
                ...cards
            ]);
        }

        // Replace existing "latest" cache entry without introducing new branch paths
        DeckService.cache = [
            ...DeckService.cache.filter(
                (c) => !(c.lang === lang && c.version === "latest")
            ),
            { lang, version: "latest", data: cards }
        ];

        return cards;
    }

    public getCardDataForEditionVersionLang(
        edition: string,
        version: string,
        lang: string
    ): Map<string, Card> {

        const cached = DeckService.cache.find(
            (c) =>
                c.edition === edition &&
                c.version === version &&
                c.lang === lang
        );

        if (cached) return cached.data;

        const cards = new Map<string, Card>();

        const cardFile = `${__dirname}${DeckService.path}${edition}-cards-${version}-${lang}.yaml`;

        if (!FileSystemHelper.hasFile(cardFile)) {
            return cards;
        }

        const yamlData = fs.readFileSync(cardFile, "utf8");
        const data: any = yaml.load(yamlData);

        let base = `data/cards/${edition}-cards-${version}-${lang}/`;

        if (!FileSystemHelper.hasDir(base)) {
            base = `data/cards/${edition}-cards-${version}-en/`;
        }

        const mapping = new MappingService().getCardMapping(edition, version);

        for (const suitIndex in data?.suits ?? []) {
            const suitObject: any = data.suits[suitIndex];
            const suitName: string = mapping?.suits?.[suitIndex]?.name ?? "";

            for (const cardIndex in suitObject?.cards ?? []) {
                const cardObject: any = suitObject.cards[cardIndex];

                cardObject.id = cardObject["id"];
                cardObject.edition = edition;
                cardObject.version = version;
                cardObject.language = lang;
                cardObject.suitName = suitName;
                cardObject.suitNameLocal = suitObject["name"];
                cardObject.suitId = suitObject["id"];
                cardObject.name = `${cardObject.suitName} (${cardObject.id})`;
                cardObject.suit = cardObject.suitName
                    .replaceAll(" ", "-")
                    .toLowerCase();
                cardObject.url = `/edition/${edition}/${cardObject.id}/${version}/${lang}`;
                cardObject.githubUrl = `${cardObject.suit}/${cardObject.id}`;

                const technicalPath = `./${base}${cardObject.githubUrl}/technical-note.md`;

                let file: string;
                try {
                    file = fs.readFileSync(technicalPath, "utf8");
                } catch (e) {
                    console.error(`Error reading file at path: ${technicalPath}`, e);
                    continue;
                }

                const parsed = fm(file);
                cardObject.concept = parsed.body;

                try {
                    const explanationPath = `./${base}${cardObject.githubUrl}/explanation.md`;
                    cardObject.summary = fm(
                        fs.readFileSync(explanationPath, "utf8")
                    ).body;
                } catch (e) {
                    console.error(
                        `Error reading explanation for: ${cardObject.githubUrl}`,
                        e
                    );
                    continue;
                }

                if (+cardIndex === 0 && +suitIndex === 0) {
                    const lastSuit = data.suits[data.suits.length - 1];
                    const lastCard = lastSuit.cards[lastSuit.cards.length - 1];
                    cardObject.prevous = lastCard.id;
                } else if (+cardIndex === 0) {
                    const prevSuit = data.suits[+suitIndex - 1];
                    cardObject.prevous =
                        prevSuit.cards[prevSuit.cards.length - 1].id;
                } else {
                    cardObject.prevous =
                        suitObject.cards[+cardIndex - 1].id;
                }

                if (
                    suitObject.cards.length === +cardIndex + 1 &&
                    data.suits.length === +suitIndex + 1
                ) {
                    cardObject.next = data.suits[0].cards[0].id;
                } else if (
                    suitObject.cards.length === +cardIndex + 1
                ) {
                    cardObject.next =
                        data.suits[+suitIndex + 1].cards[0].id;
                } else {
                    cardObject.next =
                        suitObject.cards[+cardIndex + 1].id;
                }

                cards.set(cardObject.id, cardObject);
            }
        }

        console.log(
            `Caching cards for ${edition} ${version} ${lang} - total cards: ${cards.size}`
        );

        // Replace existing cache entry without adding branch paths
        DeckService.cache = [
            ...DeckService.cache.filter(
                (c) =>
                    !(
                        c.edition === edition &&
                        c.version === version &&
                        c.lang === lang
                    )
            ),
            { edition, version, lang, data: cards }
        ];

        return cards;
    }

    public static clear(): void {
        DeckService.cache = [];
    }
}

