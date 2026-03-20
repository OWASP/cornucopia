import type { Card } from '$domain/card/card'
import { ONE } from '$lib/constants'

const NOT_FOUND = -1

export interface Link {
  name: string
  url: string
}

/**
 * Adds a link to a navigation array. 
 * Restored to fix the Rollup build error in navbar.svelte.
 */
export const AddLink = (links: Link[], name: string, url: string): void => {
  links.push({ name, url })
}

export function getNavigationLinks (currentCardId: string, deck: Card[]): { prev?: string, next?: string } {
  const index = deck.findIndex((c) => c.id === currentCardId)
  if (index === NOT_FOUND) return {}
  const { id: prevId } = deck[index - ONE] ?? {}
  const { id: nextId } = deck[index + ONE] ?? {}
  return { prev: prevId, next: nextId }
}

export function isLastCard (currentCardId: string, deck: Card[]): boolean {
  const lastIndex = deck.length - ONE
  return deck.findIndex((c) => c.id === currentCardId) === lastIndex
}