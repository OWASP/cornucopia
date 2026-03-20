import type { PageServerLoad } from './$types'
import { ONE, TWO } from '$lib/constants'

export const load: PageServerLoad = () => ({
  milestones: [
    { id: ONE, task: 'Complete Linter Fixes' },
    { id: TWO, task: 'Submit PR' }
  ]
})