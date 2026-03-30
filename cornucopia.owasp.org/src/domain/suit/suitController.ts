import { ZERO } from '$lib/constants'

export interface SuitLike {
  id: string
  name?: string
}

const NOT_FOUND = -1

export function getSuitIndex (id: string, suits: SuitLike[]): number {
  const index = suits.findIndex((s) => s.id === id)
  if (index === NOT_FOUND) return ZERO
  return index
}

export function getSuits (): SuitLike[] {
  return []
}