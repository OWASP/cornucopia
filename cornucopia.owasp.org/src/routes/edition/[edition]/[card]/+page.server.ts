import { DeckService } from '$lib/services/deckService'
import { redirect } from '@sveltejs/kit'
import type { PageServerLoad } from './$types'
import { HTTP_STATUS } from '$lib/constants'

export const load: PageServerLoad = ({ params }) => {
  const { edition, card } = params
  const version = DeckService.getLatestVersion(edition)
  const lang = 'en'
  redirect(HTTP_STATUS.FOUND, `/edition/${edition}/${card}/${version}/${lang}`)
}