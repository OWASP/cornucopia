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
    private deck: Map<string, Card>;
    private controller: MappingController;

    private static editions: Map<string, string>  = new Map<string, string>( [
        ['webapp', "OWASP Cornucopia Website App Edition"],
        ['mobileapp', "OWASP Cornucopia Mobile App Edition"],
        ['dbd', "Cornucopia Digital Benefits and Disbenefits Edition"]
    ]);

    private static category: Map<string, string>  = new Map<string, string>( [
        ['webapp', "Website Application"],
        ['mobileapp', "Mobile Application"],
        ['dbd', "Digital Benefits and Disbenefits"]
    ]);

    constructor(deck: Map<string, Card>, controller: MappingController) {
        this.deck = deck;
        this.controller = controller;
    }

    public static getEditionName(edition: string): string {
        return CreController.editions.get(edition) || edition;
    }

    public getCreMapping(edition: string, lang: string) : any {
        if (!CreController.editions.has(edition)) return {"meta": {}, "standards": []};
        let standards: Cre[] = [];
        (this.deck || []).forEach(
                (card: Card) => (card.edition == edition) && standards.push(this.generateDoc(card))
            );
        return {
            "meta": {
                "edition": CreController.editions.get(edition),
                "component": 'cards',
                "language": lang,
                "version": this.controller.getMeta()?.version
            },
            "standards": standards
        };
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