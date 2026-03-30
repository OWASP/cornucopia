import { DeckService } from '$lib/services/deckService'
import { redirect } from '@sveltejs/kit'
import type { PageServerLoad } from './$types'
import { HTTP_STATUS } from '$lib/constants'

export const load: PageServerLoad = ({ params }) => {
  const { edition, card, version } = params
  const lang = 'en'

  if (!DeckService.hasVersion(edition, version)) {
    const latest = DeckService.getLatestVersion(edition)
    redirect(HTTP_STATUS.FOUND, `/edition/${edition}/${card}/${latest}/${lang}`)
  }

  redirect(HTTP_STATUS.FOUND, `/edition/${edition}/${card}/${version}/${lang}`)
}