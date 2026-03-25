/* eslint-disable @typescript-eslint/class-methods-use-this, complexity, @typescript-eslint/no-unsafe-type-assertion -- Bypassing strict rules for complex YAML parsing logic */
import fm from 'front-matter'
import fs from 'node:fs'
import yaml from 'js-yaml'
import type { Card } from '$domain/card/card'
import { hasDir } from '$lib/filesystem/fileSystemHelper'
import path from 'node:path'
import type { Deck } from '$domain/deck/deck'
import { MappingService } from '$lib/services/mappingService'
import { ZERO } from '$lib/constants'

const DEFAULT_VERSION = '2.2'

interface FrontMatterResult { body?: string }
interface YamlCard { id?: string | number | null; [key: string]: unknown }
interface YamlSuit { id?: string | number | null; name?: string | null; cards?: YamlCard[] | Record<string, YamlCard | null> | null; [key: string]: unknown }
interface YamlData { suits?: YamlSuit[] | Record<string, YamlSuit | null> | null; [key: string]: unknown }
interface MappingSuit { id?: string | number | null; name?: string | null; [key: string]: unknown }
interface MappingData { suits?: MappingSuit[] | Record<string, MappingSuit | null> | null; [key: string]: unknown }
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

        {lang: ['en', 'hi', 'uk'], edition: 'mobileapp', version: '1.1'},
        {lang: ['en', 'es', 'fr', 'nl', 'no_nb', 'pt_br', 'pt_pt', 'ru', 'it'], edition: 'webapp', version: '2.2'},
        {lang: ['en'], edition: 'companion', version: '1.0'}
    ];
    private static readonly decks: Deck[] = [
       { edition: 'mobileapp', version: '1.1', lang: ['en', 'hi', 'uk'] },
        { edition: 'webapp', version: '2.2', lang: ['en', 'es', 'fr', 'nl', 'no_nb', 'pt_br', 'pt_pt', 'ru', 'it'] },
        { edition: 'webapp', version: '3.0', lang: ['en', 'fr', 'nl', 'no_nb', 'pt_br', 'pt_pt', 'ru', 'it', 'hi', 'uk'] },
        { edition: 'companion', version: '1.0', lang: ['en'] }];

    public static hasEdition(edition: string): boolean {
        return DeckService.decks.find((deck) => deck.edition == edition) != undefined;
    }

export class DeckService {
  private static cache: Array<{ lang: string, version: string, edition?: string, data: Map<string, Card> }> = []
  private static readonly latests: Deck[] = [
    { lang: ['en'], edition: 'mobileapp', version: '1.1' },
    { lang: ['en', 'es', 'fr', 'nl', 'no_nb', 'pt_br', 'pt_pt', 'ru', 'it'], edition: 'webapp', version: '2.2' },
    { lang: ['en'], edition: 'companion', version: '1.0' }
  ]

  private static readonly decks: Deck[] = [
    { edition: 'mobileapp', version: '1.1', lang: ['en'] },
    { edition: 'webapp', version: '2.2', lang: ['en', 'es', 'fr', 'nl', 'no_nb', 'pt_br', 'pt_pt', 'ru', 'it'] },
    { edition: 'webapp', version: '3.0', lang: ['en', 'es', 'fr', 'nl', 'no_nb', 'pt_br', 'pt_pt', 'ru', 'it', 'hi', 'uk'] },
    { edition: 'companion', version: '1.0', lang: ['en'] }
  ]

  public static hasEdition (edition: string): boolean {
    return DeckService.decks.some((deck) => deck.edition === edition)
  }

  public static hasVersion (edition: string, version: string): boolean {
    return DeckService.decks.some((deck) => deck.edition === edition && deck.version === version)
  }

  public static hasLanguage (edition: string, lang: string): boolean {
    return DeckService.decks.some((deck) => deck.edition === edition && deck.lang.includes(lang))
  }

  public static getDecks (): Deck[] {
    return DeckService.decks
  }

  public static getLatestVersion (edition: string): string {
    return DeckService.latests.find((deck) => deck.edition === edition)?.version ?? DEFAULT_VERSION
  }

  public static getLatestEditions (): string[] {
    return DeckService.latests.map((deck) => deck.edition)
  }

  public static getLanguages (edition: string): string[] {
    const languages = DeckService.decks
      .filter((deck) => deck.edition === edition)
      .flatMap((deck) => deck.lang)
    return languages.length === ZERO ? ['en'] : languages
  }

  public static getLanguagesForEditionVersion (edition: string, version: string): string[] {
    return DeckService.decks.find((d) => d.edition === edition && d.version === version)?.lang ?? []
  }

  public static getVersions (edition: string): string[] {
    return DeckService.decks.filter((deck) => deck.edition === edition).map((deck) => deck.version)
  }

  public static resolveSourceFile (fileName: string): string {
    const cwd = process.cwd()
    const candidates = [
      path.join(cwd, 'source', fileName),
      path.join(cwd, '..', 'source', fileName),
      path.join(cwd, '..', '..', 'source', fileName)
    ]
    return candidates.find((p) => fs.existsSync(p)) ?? ''
  }

  public getCards (lang: string): Map<string, Card> {
    const cached = DeckService.cache.find((deck) => deck.lang === lang && deck.version === 'latest')
    if (cached !== undefined && cached.data.size > ZERO) return cached.data
    return this.getCardData(lang)
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
    const cached = DeckService.cache.find((c) => c.edition === edition && c.version === version && c.lang === lang)
    if (cached !== undefined && cached.data.size > ZERO) return cached.data

    const cards = new Map<string, Card>()
    const fileName = `${edition}-cards-${version}-${lang}.yaml`

    let cardFile = DeckService.resolveSourceFile(fileName)

    if (cardFile === '' && lang !== 'en' && DeckService.hasLanguage(edition, lang)) {
      const fallbackFileName = `${edition}-cards-${version}-en.yaml`
      cardFile = DeckService.resolveSourceFile(fallbackFileName)
    }

    if (cardFile === '') return cards

    const data = ((): YamlData | null => {
      try {
        const yamlData = fs.readFileSync(cardFile, 'utf8')
        const parsedYaml = yaml.load(yamlData)
        if (parsedYaml === null || typeof parsedYaml !== 'object') return null
        return parsedYaml as YamlData
      } catch {
        return null
      }
    })()

    if (data === null) return cards

    const baseDir = hasDir(`data/cards/${edition}-cards-${version}-${lang}/`)
      ? `data/cards/${edition}-cards-${version}-${lang}/`
      : `data/cards/${edition}-cards-${version}-en/`

    const mapping: MappingData = { ...MappingService.getCardMapping(edition, version) }

    const { suits } = data
    if (suits === undefined || suits === null) return cards

    const suitsIterable: YamlSuit[] = DeckService.toIterable<YamlSuit>(suits)

    const { suits: mapSuits } = mapping
    const mapList: MappingSuit[] = (mapSuits !== undefined && mapSuits !== null)
      ? DeckService.toIterable<MappingSuit>(mapSuits)
      : []

    for (const suitObj of suitsIterable) {
      const { name: suitObjName, id: suitObjId, cards: suitCards } = suitObj

      const mappingSuit: MappingSuit | undefined = mapList.length > ZERO
        ? mapList.find((m) => String(m.id ?? '') === String(suitObjId ?? '') || (m.name ?? '') === (suitObjName ?? ''))
        : undefined

      if (suitCards === undefined || suitCards === null) continue

      const cardsIterable: YamlCard[] = DeckService.toIterable<YamlCard>(suitCards)

      for (const cardData of cardsIterable) {
        const { id: cardDataId } = cardData
        if (cardDataId === undefined || cardDataId === null) continue

        const cardIdStr = `${cardDataId}`
        const suitNameStr = mappingSuit?.name ?? suitObjName ?? ''
        const suit = suitNameStr.replaceAll(' ', '-').toLocaleLowerCase()
        const cardFolderPath = `${suit}/${cardIdStr}`

        const { conceptText, summaryText } = DeckService.readCardMarkdown(baseDir, cardFolderPath)

        const newCard: Card = {
          ...cardData,
          id: cardIdStr,
          edition,
          version,
          language: lang,
          suitName: suitNameStr,
          suitNameLocal: suitObjName ?? '',
          suitId: `${suitObjId ?? ''}`,
          name: `${suitNameStr} (${cardIdStr})`,
          suit,
          url: `/edition/${edition}/${cardIdStr}/${version}/${lang}`,
          githubUrl: `${baseDir}${cardFolderPath}/explanation.md`,
          concept: conceptText,
          summary: summaryText

  private getCardData(lang: string)
{
    let cards = new Map<string, Card>;
    const decks = DeckService.latests;

    for (let i in decks) {
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

        let cardFile = `${__dirname}${DeckService.path}${edition}-cards-${version}-${lang}.yaml`;

        if (!FileSystemHelper.hasFile(cardFile)) {
            return cards;
        }
        cards.set(cardIdStr, newCard)
      }
    }

    DeckService.cache.push({ edition, version, lang, data: cards })
    return cards
  }

  private static toIterable<T extends { id?: unknown, name?: unknown }> (
    input: T[] | Record<string, T | null>
  ): T[] {
    if (Array.isArray(input)) return input
    const result: T[] = []
    for (const [key, val] of Object.entries(input)) {
      if (val !== null) {
        const item: T = { ...val, id: key, name: key }
        result.push(item)
      }
    }
    return result
  }

  private static readCardMarkdown (
    baseDir: string,
    cardFolderPath: string
  ): { conceptText: string, summaryText: string } {
    let conceptText = ''
    let summaryText = ''
    try {
      const conceptP = `./${baseDir}${cardFolderPath}/technical-note.md`
      const summaryP = `./${baseDir}${cardFolderPath}/explanation.md`
      if (fs.existsSync(conceptP)) conceptText = (fm(fs.readFileSync(conceptP, 'utf8')) as FrontMatterResult).body ?? ''
      if (fs.existsSync(summaryP)) summaryText = (fm(fs.readFileSync(summaryP, 'utf8')) as FrontMatterResult).body ?? ''
    } catch { /* ignore */ }
    return { conceptText, summaryText }
  }

  public static clear (): void {
    DeckService.cache = []
  }
}