import { getAuthors } from '../../domain/author/authorController.js'
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = () => ({
  authors: getAuthors()
})