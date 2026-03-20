import { DeckService } from '$lib/services/deckService'
import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper'
import { MappingService } from '$lib/services/mappingService'
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = () => {
  const deckService = new DeckService()
  const decks = new Map<string, unknown>()
  const lang = 'en'

  const mobileCards = deckService.getCardDataForEditionVersionLang(
    'mobileapp', DeckService.getLatestVersion('mobileapp'), lang)
  const webappCards = deckService.getCardDataForEditionVersionLang(
    'webapp', DeckService.getLatestVersion('webapp'), lang)
  const companionCards = deckService.getCardDataForEditionVersionLang(
    'companion', DeckService.getLatestVersion('companion'), lang)

  return {
    decks: decks.set(lang, new Map([...mobileCards, ...webappCards, ...companionCards])),
    mappingData: (new MappingService()).getCardMappingForLatestEdtions(),
    content: FileSystemHelper.getDataFromPath('data/website/pages/cards')
  }
}