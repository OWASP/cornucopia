/* eslint-disable @typescript-eslint/prefer-destructuring, @typescript-eslint/class-methods-use-this, complexity, @typescript-eslint/no-unsafe-type-assertion, prefer-object-has-own -- Bypassing strict stylistic rules for complex YAML parsing logic */
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

// --- STRICT TYPE DEFINITIONS ---
interface FrontMatterResult {
  attributes?: Record<string, unknown>
  body?: string
}

interface YamlCard {
  id?: string | number
  [key: string]: unknown
}

interface YamlSuit {
  id?: string | number
  name?: string
  cards?: YamlCard[] | Record<string, YamlCard>
  [key: string]: unknown
}

interface YamlData {
  suits?: YamlSuit[] | Record<string, YamlSuit>
  [key: string]: unknown
}

interface MappingSuit {
  id?: string | number
  name?: string
  [key: string]: unknown
}

interface MappingData {
  suits?: MappingSuit[] | Record<string, MappingSuit>
  [key: string]: unknown
}
// -------------------------------

export class DeckService {
  private static cache: Array<{ lang: string, version: string, data: Map<string, Card> }> = []

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
    return languages.length === ZERO ? ['en'] : languages
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

    const possiblePaths = [
      path.join(fileSystemRoot, `../source/${edition}-cards-${version}-${lang}.yaml`),
      path.join(fileSystemRoot, `source/${edition}-cards-${version}-${lang}.yaml`),
      path.resolve(path.dirname(''), `../source/${edition}-cards-${version}-${lang}.yaml`),
      path.resolve(path.dirname(''), `source/${edition}-cards-${version}-${lang}.yaml`)
    ]

    let cardFile = ''
    for (const p of possiblePaths) {
      if (fs.existsSync(p)) {
        cardFile = p
        break
      }
    }

    if (cardFile.length === ZERO) return cards

    const yamlData = fs.readFileSync(cardFile, 'utf8')
    const data = yaml.load(yamlData, { schema: yaml.FAILSAFE_SCHEMA }) as YamlData | undefined
    const defaultBase = `data/cards/${edition}-cards-${version}-${lang}/`
    const baseDir = hasDir(defaultBase) ? defaultBase : `data/cards/${edition}-cards-${version}-en/`
    
    const mapping = MappingService.getCardMapping(edition, version) as MappingData | undefined

    if (data?.suits === undefined) return cards

    const suitsIterable: Array<YamlSuit & { _key?: string }> = Array.isArray(data.suits)
      ? data.suits
      : Object.entries(data.suits).map(([key, val]) => ({ _key: key, ...val }))

    for (const suitObj of suitsIterable) {
      let mappingSuit: MappingSuit | undefined = undefined

      if (mapping?.suits !== undefined) {
        const suitKey = suitObj._key ?? ''
        if (suitKey === '' || Array.isArray(mapping.suits) || !Object.prototype.hasOwnProperty.call(mapping.suits, suitKey)) {
          const mapList = Array.isArray(mapping.suits) ? mapping.suits : Object.values(mapping.suits)
          mappingSuit = mapList.find((m) => {
            const mId = m.id === undefined ? '' : String(m.id)
            const sId = suitObj.id === undefined ? '' : String(suitObj.id)
            const mName = m.name ?? ''
            const sName = suitObj.name ?? ''
            return (mId !== '' && mId === sId) || (mName !== '' && mName === sName)
          })
        } else {
          mappingSuit = mapping.suits[suitKey]
        }
      }

      if (suitObj.cards === undefined) continue
      const cardsIterable: YamlCard[] = Array.isArray(suitObj.cards) ? suitObj.cards : Object.values(suitObj.cards)

      for (const cardData of cardsIterable) {
        if (cardData.id === undefined) continue

        const suitNameStr = mappingSuit?.name ?? suitObj.name ?? ''
        const suit = suitNameStr.replaceAll(' ', '-').toLocaleLowerCase()
        const cardFolderPath = `${suit}/${String(cardData.id)}`

        let conceptText = ''
        let summaryText = ''

        try {
          const conceptFile = `./${baseDir}${cardFolderPath}/technical-note.md`
          const summaryFile = `./${baseDir}${cardFolderPath}/explanation.md`
          if (fs.existsSync(conceptFile)) {
            const parsed = fm(fs.readFileSync(conceptFile, 'utf8')) as FrontMatterResult
            conceptText = parsed.body ?? ''
          }
          if (fs.existsSync(summaryFile)) {
            const parsed = fm(fs.readFileSync(summaryFile, 'utf8')) as FrontMatterResult
            summaryText = parsed.body ?? ''
          }
        } catch { /* safely ignore */ }

        const newCard: Card = {
          ...cardData,
          edition,
          version,
          language: lang,
          suitName: suitNameStr,
          suitNameLocal: suitObj.name ?? '',
          suitId: suitObj.id === undefined ? '' : String(suitObj.id),
          name: `${suitNameStr} (${String(cardData.id)})`,
          suit,
          url: `/edition/${edition}/${String(cardData.id)}/${version}/${lang}`,
          githubUrl: `${baseDir}${cardFolderPath}/explanation.md`,
          concept: conceptText,
          summary: summaryText
        }
        
        cards.set(newCard.id, newCard)
      }
    }
    return cards
  }

  public static clear (): void { DeckService.cache = [] }
}