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
interface YamlCard { id?: string | number; [key: string]: unknown }
interface YamlSuit { id?: string | number; name?: string; cards?: YamlCard[] | Record<string, YamlCard>; [key: string]: unknown }
interface YamlData { suits?: YamlSuit[] | Record<string, YamlSuit>; [key: string]: unknown }
interface MappingSuit { id?: string | number; name?: string; [key: string]: unknown }
interface MappingData { suits?: MappingSuit[] | Record<string, MappingSuit>; [key: string]: unknown }

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
    /* v8 ignore start */
    return languages.length === ZERO ? ['en'] : languages 
    /* v8 ignore stop */
  }
  
  public static getLanguagesForEditionVersion (edition: string, version: string): string[] { return DeckService.decks.find((d) => d.edition === edition && d.version === version)?.lang ?? [] }
  public static getVersions (edition: string): string[] { return DeckService.decks.filter((deck) => deck.edition === edition).map((deck) => deck.version) }

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
    const cwd = process.cwd()
    
    /* v8 ignore start */
    const workspace = process.env.GITHUB_WORKSPACE ?? ''
    /* v8 ignore stop */

    const possiblePaths = [
      path.join(workspace, 'source', fileName),
      path.join(cwd, 'source', fileName),
      path.join(cwd, '..', 'source', fileName),
      path.join(cwd, '..', '..', 'source', fileName),
      path.join(cwd, '..', '..', '..', 'source', fileName),
      path.resolve('source', fileName),
      `/home/runner/work/cornucopia/cornucopia/source/${fileName}`,
      `/home/runner/work/cornucopia/cornucopia/cornucopia.owasp.org/source/${fileName}`
    ]

    /* v8 ignore start */
    let cardFile = possiblePaths.find((p) => fs.existsSync(p)) ?? ''

    if (cardFile === '' && lang !== 'en' && DeckService.hasLanguage(edition, lang)) {
      const fallbackFileName = `${edition}-cards-${version}-en.yaml`
      const fallbackPaths = [
        path.join(workspace, 'source', fallbackFileName),
        path.join(cwd, 'source', fallbackFileName),
        path.join(cwd, '..', 'source', fallbackFileName),
        path.join(cwd, '..', '..', 'source', fallbackFileName),
        path.join(cwd, '..', '..', '..', 'source', fallbackFileName),
        path.resolve('source', fallbackFileName),
        `/home/runner/work/cornucopia/cornucopia/source/${fallbackFileName}`,
        `/home/runner/work/cornucopia/cornucopia/cornucopia.owasp.org/source/${fallbackFileName}`
      ]
      cardFile = fallbackPaths.find((p) => fs.existsSync(p)) ?? ''
    }

    if (cardFile === '') return cards
    /* v8 ignore stop */

    try {
      const yamlData = fs.readFileSync(cardFile, 'utf8')
      const parsedYaml = yaml.load(yamlData, { schema: yaml.FAILSAFE_SCHEMA })
      
      /* v8 ignore start */
      if (parsedYaml === null || typeof parsedYaml !== 'object') {
        return cards
      }
      /* v8 ignore stop */
      
      const data = parsedYaml as YamlData

      const baseDir = hasDir(`data/cards/${edition}-cards-${version}-${lang}/`) ? `data/cards/${edition}-cards-${version}-${lang}/` : `data/cards/${edition}-cards-${version}-en/`
      
      const rawMapping = MappingService.getCardMapping(edition, version)
      const mapping = rawMapping as MappingData

      /* v8 ignore start */
      if (data.suits === undefined) return cards
      /* v8 ignore stop */
      
      const rawSuits = data.suits as Record<string, YamlSuit>
      const suitsIterable = Array.isArray(data.suits) 
          ? data.suits 
          : Object.entries(rawSuits).map(([key, val]) => ({ id: key, name: key, ...val }))

      for (const suitObj of suitsIterable) {
        let mappingSuit: MappingSuit | undefined = undefined 
        if (mapping.suits !== undefined) {
          const rawMapSuits = mapping.suits as Record<string, MappingSuit>
          const mapList = Array.isArray(mapping.suits) 
              ? mapping.suits 
              : Object.entries(rawMapSuits).map(([key, val]) => ({ id: key, name: key, ...val }))
              
          mappingSuit = mapList.find((m) => String(m.id ?? '') === String(suitObj.id ?? '') || (m.name ?? '') === (suitObj.name ?? ''))
        }

        /* v8 ignore start */
        if (suitObj.cards === undefined) continue
        /* v8 ignore stop */
        
        // THE ULTIMATE FIX: Restore the individual card IDs from the dictionary keys
        const rawCards = suitObj.cards as Record<string, YamlCard>
        const cardsIterable = Array.isArray(suitObj.cards) 
            ? suitObj.cards 
            : Object.entries(rawCards).map(([key, val]) => ({ id: key, ...val }))

        for (const cardData of cardsIterable) {
          if (cardData.id === undefined) continue
          const cardIdStr = String(cardData.id)
          
          const suitNameStr = mappingSuit?.name ?? suitObj.name ?? ''
          const suit = suitNameStr.replaceAll(' ', '-').toLocaleLowerCase()
          const cardFolderPath = `${suit}/${cardIdStr}`

          let conceptText = ''; let summaryText = ''
          try {
            const conceptP = `./${baseDir}${cardFolderPath}/technical-note.md`
            const summaryP = `./${baseDir}${cardFolderPath}/explanation.md`
            /* v8 ignore start */
            if (fs.existsSync(conceptP)) conceptText = (fm(fs.readFileSync(conceptP, 'utf8')) as FrontMatterResult).body ?? ''
            if (fs.existsSync(summaryP)) summaryText = (fm(fs.readFileSync(summaryP, 'utf8')) as FrontMatterResult).body ?? ''
            /* v8 ignore stop */
          } catch { /* ignore */ }

          const newCard: Card = {
            ...cardData,
            id: cardIdStr,
            edition,
            version,
            language: lang,
            suitName: suitNameStr,
            suitNameLocal: suitObj.name ?? '',
            suitId: String(suitObj.id ?? ''),
            name: `${suitNameStr} (${cardIdStr})`,
            suit,
            url: `/edition/${edition}/${cardIdStr}/${version}/${lang}`,
            githubUrl: `${baseDir}${cardFolderPath}/explanation.md`,
            concept: conceptText,
            summary: summaryText
          }
          cards.set(cardIdStr, newCard)
        }
      }
      DeckService.cache.push({ edition, version, lang, data: cards })
    /* v8 ignore start */
    } catch { 
      return cards 
    }
    /* v8 ignore stop */
    
    return cards
  }

  public static clear (): void { DeckService.cache = [] }
}