import { DeckService } from '$lib/services/deckService'
import { redirect } from '@sveltejs/kit'
import type { PageServerLoad } from './$types'
import { HTTP_STATUS } from '$lib/constants'

export const load: PageServerLoad = ({ params }) => {
  const {edition} = params
  const version = DeckService.getLatestVersion(edition)
  const lang = 'en'
  redirect(HTTP_STATUS.PERMANENT_REDIRECT, `/edition/${edition}/J/${version}/${lang}`)
}