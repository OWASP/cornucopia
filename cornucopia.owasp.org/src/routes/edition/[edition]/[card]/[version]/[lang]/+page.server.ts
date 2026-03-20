import { DeckService } from '$lib/services/deckService'
import { error } from '@sveltejs/kit'
import type { PageServerLoad } from './$types'
import { HTTP_STATUS } from '$lib/constants'

export const load: PageServerLoad = ({ params }) => {
  const { edition, card, version, lang } = params

  if (edition === '' || card === '' || version === '' || lang === '') {
    throw new Error('Missing required parameters')
  }

  const service = new DeckService()
  const deck = service.getCardDataForEditionVersionLang(edition, version, lang)
  const cardData = deck.get(card)

  if (cardData === undefined) {
    error(HTTP_STATUS.NOT_FOUND, `Card ${card} not found in ${edition} edition`)
  }

  return { card: cardData, edition, version, lang }
}