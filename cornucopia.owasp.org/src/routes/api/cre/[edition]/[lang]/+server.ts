import { json } from '@sveltejs/kit'
import { DeckService } from '$lib/services/deckService'
import type { RequestHandler } from './$types'
import { HTTP_STATUS } from '$lib/constants'

export const GET: RequestHandler = ({ params }) => {
  const { edition, lang } = params
  if (edition === '' || lang === '') {
    return json({ error: 'Missing params' }, { status: HTTP_STATUS.BAD_REQUEST })
  }

  const service = new DeckService()
  const version = DeckService.getLatestVersion(edition)
  const cards = service.getCardDataForEditionVersionLang(edition, version, lang)

  return json(Object.fromEntries(cards))
}