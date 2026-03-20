import type { MappingController } from '$domain/mapping/mappingController'

interface CardData {
  id: string
  owasp_cre?: string[]
}

interface CreEntry {
  card: string
  cre: string[]
}

interface CreMapping {
  edition: string
  lang: string
  mappings: CreEntry[]
}

function isRecord(obj: unknown): obj is Record<string, unknown> {
  return typeof obj === 'object' && obj !== null && !Array.isArray(obj);
}

function isCreMap(obj: unknown): obj is { owasp_cre: string[] } {
  if (isRecord(obj)) {
    // Aliasing to camelCase to pass the naming-convention rule
    const { owasp_cre: owaspCre } = obj;
    return Array.isArray(owaspCre);
  }
  return false;
}

export class CreController {
  private readonly cards: Map<string, CardData>
  private readonly mapping: MappingController

  constructor (cards: Map<string, CardData>, mapping: MappingController) {
    this.cards = cards
    this.mapping = mapping
  }

  public getCreMapping (edition: string, lang: string): CreMapping {
    const mappings: CreEntry[] = []
    
    for (const card of this.cards.values()) {
      const { id: cardId } = card
      const map = this.mapping.getWebAppCardMappings(cardId)
      
      if (isCreMap(map)) {
        // Aliasing to camelCase to pass the naming-convention rule
        const { owasp_cre: owaspCre } = map;
        mappings.push({ card: cardId, cre: owaspCre });
      }
    }
    
    return { edition, lang, mappings }
  }
}