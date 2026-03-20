import { DeckService } from '$lib/services/deckService'
import { MappingService } from '$lib/services/mappingService'
import { getSuits } from '../domain/suit/suitController'
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = () => ({
  suits: getSuits(),
  cards: (new DeckService()).getCards('en'),
  mappingData: (new MappingService()).getCardMappingForLatestEdtions()
})