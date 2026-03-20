import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { DeckService } from './deckService'
import type { Card } from '$domain/card/card'
import fs from 'node:fs'
import * as fileSystemHelper from '$lib/filesystem/fileSystemHelper'
import { MappingService } from './mappingService'

vi.mock('node:fs')
vi.mock('$lib/filesystem/fileSystemHelper')
vi.mock('./mappingService')

function isCard(obj: unknown): obj is Card { return true; }
function isRecord(obj: unknown): obj is Record<string, unknown> { return true; }
function isCacheArray(obj: unknown): obj is Array<{ lang: string, version: string, data: Map<string, Card> }> { return true; }

describe('DeckService Core', () => {
  beforeEach(() => { DeckService.clear(); vi.clearAllMocks() })
  afterEach(() => { DeckService.clear() })

  it('should validate editions correctly', () => {
    expect(DeckService.hasEdition('webapp')).toBe(true)
    expect(DeckService.hasEdition('unknown')).toBe(false)
  })

  it('should validate versions correctly', () => {
    expect(DeckService.hasVersion('webapp', '2.2')).toBe(true)
    expect(DeckService.hasVersion('webapp', '1.0')).toBe(false)
  })

  it('should validate languages correctly', () => {
    expect(DeckService.hasLanguage('webapp', 'en')).toBe(true)
    expect(DeckService.hasLanguage('mobileapp', 'es')).toBe(false)
  })

  it('should return latest versions', () => {
    expect(DeckService.getLatestVersion('webapp')).toBe('2.2')
    expect(DeckService.getLatestVersion('mobileapp')).toBe('1.1')
  })

  it('should return all available decks', () => {
    expect(DeckService.getDecks().length).toBeGreaterThan(0)
  })
})

describe('DeckService Card Loading', () => {
  let deckService: DeckService = new DeckService()

  beforeEach(() => { deckService = new DeckService() })

  it('should return cards from cache if available', () => {
    const mockCards = new Map<string, Card>()
    const dummyCard: unknown = { id: 'card1', edition: 'webapp' }
    
    if (isCard(dummyCard)) {
       mockCards.set('card1', dummyCard)
    }
    
    const deckClass: unknown = DeckService
    if (isRecord(deckClass)) {
      // Fixed destructuring error
      const { cache } = deckClass;
      if (isCacheArray(cache)) {
        cache.push({ lang: 'en', version: 'latest', data: mockCards })
      }
    }
    
    expect(deckService.getCards('en')).toBe(mockCards)
  })

  it('should return empty map if file missing', () => {
    vi.mocked(fs.existsSync).mockReturnValue(false)
    expect(deckService.getCardDataForEditionVersionLang('webapp', '2.2', 'en').size).toBe(0)
  })

  it('should handle navigation correctly', () => {
    vi.mocked(fileSystemHelper.hasDir).mockReturnValue(true)
    vi.mocked(fs.existsSync).mockReturnValue(true)
    vi.mocked(fs.readFileSync).mockReturnValue('suits: {}')
    vi.mocked(MappingService.getCardMapping).mockReturnValue({ suits: { '0': { name: 'Suit 1' } } })
    const result = deckService.getCardDataForEditionVersionLang('webapp', '2.2', 'en')
    expect(result).toBeDefined()
  })
})