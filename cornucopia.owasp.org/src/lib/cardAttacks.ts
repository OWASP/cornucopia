import type { Card } from '$domain/card/card'
import { ZERO, ONE, TWO } from '$lib/constants'

export interface CardAttack {
  id: string
  name: string
  description: string
}

export function getCardAttacks (card: Card): CardAttack[] {
  const attacks: CardAttack[] = []
  if (card.desc === '') return attacks
  const lines = card.desc.split('\n')
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