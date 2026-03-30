import type { Card } from '$domain/card/card'
import { ZERO, ONE, TWO } from '$lib/constants'

export interface CardAttack {
  id: string
  name: string
  description: string
}

// Defining 'Attack' as an alias to 'CardAttack' to satisfy the Svelte component imports
export type Attack = CardAttack;

/**
 * Restored and Renamed: Returns security attacks associated with a card.
 * Renamed to GetCardAttacks to match the project-wide naming convention and fix build errors.
 */
export function GetCardAttacks (card: Card): Attack[] {
  const attacks: Attack[] = []
  if (card.summary === '') return attacks
  
  const lines = card.summary.split('\n')
  for (const line of lines) {
    const trimmed = line.trim()
    if (trimmed.startsWith('-')) {
      const parts = trimmed.split(':')
      if (parts.length >= TWO) {
        attacks.push({
          id: parts[ZERO].replace('-', '').trim(),
          name: parts[ZERO].trim(),
          description: parts.slice(ONE).join(':').trim()
        })
      }
    }
  }
  return attacks
}