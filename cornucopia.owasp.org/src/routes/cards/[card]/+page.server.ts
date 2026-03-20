import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper'
import { DeckService } from '$lib/services/deckService'
import type { PageServerLoad } from './$types'
import type { Route } from '../../../domain/routes/route'
import type { Card } from '$domain/card/card'
import { MappingService } from '$lib/services/mappingService'
import { error } from '@sveltejs/kit'
import { HTTP_STATUS } from '$lib/constants'

function legacyCardCodeFix (card: string): string {
  return card
    .replace('COM', 'CM')
    .replace('CO', 'C')
    .replace('DVE', 'VE')
    .replace('AC', 'AT')
}

export const load: PageServerLoad = (({ params }) => {
  const lang = 'en'
  const deckService = new DeckService()

  const mobileCards = deckService.getCardDataForEditionVersionLang(
    'mobileapp', DeckService.getLatestVersion('mobileapp'), lang)
  const webappCards = deckService.getCardDataForEditionVersionLang(
    'webapp', DeckService.getLatestVersion('webapp'), lang)

  const cards = new Map([...mobileCards, ...webappCards])
  const decks = new Map([['en', cards]])
  const fixedCode = legacyCardCodeFix(params.card.toUpperCase())
  const card: Card | undefined = cards.get(fixedCode)

  if (card === undefined) {
    error(HTTP_STATUS.NOT_FOUND, `Card not found: ${fixedCode}`)
  }

  const { edition } = card
  const versions = DeckService.getVersions(edition)

  return {
    card: fixedCode,
    decks,
    versions,
    routes: new Map<string, Route[]>([
      ['ASVSRoutes', FileSystemHelper.ASVSRouteMap()]
    ]),
    mappingData: new MappingService().getCardMappingForLatestEdtions(),
    languages: DeckService.getLanguages(card.edition)
  }
})