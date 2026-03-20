interface MappingData {
  suits?: Record<string, SuitData>
  meta?: Record<string, unknown>
}

interface SuitData {
  cards?: Record<string, unknown>
}

export class MappingController {
  private readonly data: MappingData

  constructor (data: MappingData) {
    this.data = data
  }

  public getWebAppCardMappings (cardId: string): unknown {
    if (this.data.suits === undefined) return {}
    const suits = Object.values(this.data.suits)
    for (const suit of suits) {
      if (suit.cards?.[cardId] !== undefined) {
        return suit.cards[cardId]
      }
    }
    return {}
  }

  public getMeta (): Record<string, unknown> {
    return this.data.meta ?? {}
  }
}