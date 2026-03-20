/* eslint-disable */
import fm from 'front-matter'
import fs from 'node:fs'
import yaml from 'js-yaml'
import type { Card } from '$domain/card/card'
import { hasDir, fileSystemRoot } from '$lib/filesystem/fileSystemHelper'
import path from 'node:path'
import type { Deck } from '$domain/deck/deck'
import { MappingService } from '$lib/services/mappingService'
import { ZERO } from '$lib/constants'

const DEFAULT_VERSION = '2.2'

export class DeckService {
  private static cache: any[] = []

  private static readonly latests: Deck[] = [
    { lang: ['en'], edition: 'mobileapp', version: '1.1' },
    { lang: ['en', 'es', 'fr', 'nl', 'no_nb', 'pt_br', 'pt_pt', 'ru', 'it'], edition: 'webapp', version: '2.2' },
    { lang: ['en'], edition: 'companion', version: '1.0' }
  ]

  private static readonly decks: Deck[] = [
    { edition: 'mobileapp', version: '1.1', lang: ['en'] },
    { edition: 'webapp', version: '2.2', lang: ['en', 'es', 'fr', 'nl', 'no_nb', 'pt_br', 'pt_pt', 'ru', 'it'] },
    { edition: 'webapp', version: '3.0', lang: ['en', 'fr', 'nl', 'no_nb', 'pt_br', 'pt_pt', 'ru', 'it', 'hi', 'uk'] },
    { edition: 'companion', version: '1.0', lang: ['en'] }
  ]

  public static hasEdition (edition: string): boolean { return DeckService.decks.some((deck) => deck.edition === edition) }
  public static hasVersion (edition: string, version: string): boolean { return DeckService.decks.some((deck) => deck.edition === edition && deck.version === version) }
  public static hasLanguage (edition: string, lang: string): boolean { return DeckService.decks.some((deck) => deck.edition === edition && deck.lang.includes(lang)) }
  public static getDecks (): Deck[] { return DeckService.decks }
  public static getLatestVersion (edition: string): string { return DeckService.latests.find((deck) => deck.edition === edition)?.version ?? DEFAULT_VERSION }
  public static getLatestEditions (): string[] { return DeckService.latests.map((deck) => deck.edition) }
  public static getLanguages (edition: string): string[] {
    const languages = DeckService.decks.filter((deck) => deck.edition === edition).flatMap((deck) => deck.lang)
    return languages.length !== ZERO ? languages : ['en']
  }
  public static getLanguagesForEditionVersion (edition: string, version: string): string[] { return DeckService.decks.find((d) => d.edition === edition && d.version === version)?.lang ?? [] }
  public static getVersions (edition: string): string[] { return DeckService.decks.filter((deck) => deck.edition === edition).map((deck) => deck.version) }

  public getCards (lang: string): Map<string, Card> {
    const cached = DeckService.cache.find((deck) => deck.lang === lang && deck.version === 'latest')
    return cached?.data ?? this.getCardData(lang)
  }

  private getCardData (lang: string): Map<string, Card> {
    let cards = new Map<string, Card>()
    for (const deck of DeckService.latests) {
      cards = new Map([...this.getCardDataForEditionVersionLang(deck.edition, deck.version, lang), ...cards])
    }
    DeckService.cache.push({ lang, data: cards, version: 'latest' })
    return cards
  }

  public getCardDataForEditionVersionLang (edition: string, version: string, lang: string): Map<string, Card> {
    const cards = new Map<string, Card>()

    // 1. Bulletproof File Hunting: Using your actual root so it never gets lost again
    const possiblePaths = [
      path.join(fileSystemRoot, `../source/${edition}-cards-${version}-${lang}.yaml`),
      path.join(fileSystemRoot, `source/${edition}-cards-${version}-${lang}.yaml`),
      path.resolve(path.dirname(''), `../source/${edition}-cards-${version}-${lang}.yaml`),
      path.resolve(path.dirname(''), `source/${edition}-cards-${version}-${lang}.yaml`)
    ];

    let cardFile = '';
    for (const p of possiblePaths) {
      if (fs.existsSync(p)) {
        cardFile = p;
        break;
      }
    }

    if (!cardFile) return cards;

    const yamlData = fs.readFileSync(cardFile, 'utf8');
    const data: any = yaml.load(yamlData, { schema: yaml.FAILSAFE_SCHEMA });
    const defaultBase = `data/cards/${edition}-cards-${version}-${lang}/`;
    const baseDir = hasDir(defaultBase) ? defaultBase : `data/cards/${edition}-cards-${version}-en/`;
    const mapping: any = MappingService.getCardMapping(edition, version);

    if (!data || !data.suits) return cards;

    // 2. Bulletproof Iteration: Automatically handles YAML arrays OR objects without crashing
    const suitsIterable = Array.isArray(data.suits)
      ? data.suits
      : Object.keys(data.suits).map(key => ({ _key: key, ...data.suits[key] }));

    for (const suitObj of suitsIterable) {
      if (!suitObj) continue;

      let mappingSuit = null;
      if (mapping && mapping.suits) {
        if (suitObj._key && mapping.suits[suitObj._key]) {
          mappingSuit = mapping.suits[suitObj._key];
        } else {
          const mapList = Array.isArray(mapping.suits) ? mapping.suits : Object.values(mapping.suits);
          mappingSuit = mapList.find((m: any) => m.id === suitObj.id || m.name === suitObj.name);
        }
      }
      if (!mappingSuit) mappingSuit = suitObj;

      if (!suitObj.cards) continue;
      const cardsIterable = Array.isArray(suitObj.cards) ? suitObj.cards : Object.values(suitObj.cards);

      for (const cardData of cardsIterable as any[]) {
        if (!cardData || cardData.id == null) continue;

        const suitNameStr = String(mappingSuit.name || suitObj.name || '');
        const suit = suitNameStr.replaceAll(' ', '-').toLocaleLowerCase();
        const cardFolderPath = `${suit}/${cardData.id}`;

        let conceptText = '';
        let summaryText = '';

        try {
          const conceptFile = `./${baseDir}${cardFolderPath}/technical-note.md`;
          const summaryFile = `./${baseDir}${cardFolderPath}/explanation.md`;
          if (fs.existsSync(conceptFile)) {
            const parsed = fm(fs.readFileSync(conceptFile, 'utf8')) as any;
            conceptText = String(parsed.body || '');
          }
          if (fs.existsSync(summaryFile)) {
            const parsed = fm(fs.readFileSync(summaryFile, 'utf8')) as any;
            summaryText = String(parsed.body || '');
          }
        } catch { /* safely ignore */ }

        const newCard: Card = {
          ...cardData,
          edition,
          version,
          language: lang,
          suitName: suitNameStr,
          suitNameLocal: String(suitObj.name || ''),
          suitId: String(suitObj.id || ''),
          name: `${suitNameStr} (${cardData.id})`,
          suit,
          url: `/edition/${edition}/${cardData.id}/${version}/${lang}`,
          githubUrl: `${baseDir}${cardFolderPath}/explanation.md`,
          concept: conceptText,
          summary: summaryText
        };
        cards.set(newCard.id, newCard);
      }
    }
    return cards;
  }

  public static clear (): void { DeckService.cache = [] }
}