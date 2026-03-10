import type { Card } from "../card/card";
import type { MappingController } from "../mapping/mappingController";

export type Cre  = 
{
    doctype: string; 
    name: any; 
    section: string; 
    description: string; 
    sectionID: string; 
    hyperlink: string; 
    links: CreLink[];
    tags: never[];
    tooltype: string;
}

export type CreLink = 
{
    document: CreDocument;
    ltype: string;
}

export type CreDocument = 
{
    doctype: string;
    id: string;
}


export class CreController {
    private deck: Map<string, Card>;
    private controller: MappingController;

    private static editions: Map<string, string>  = new Map<string, string>( [
        ['webapp', "OWASP Cornucopia Website App Edition"],
        ['mobileapp', "OWASP Cornucopia Mobile App Edition"]

    ]);

    private static category: Map<string, string>  = new Map<string, string>( [
        ['webapp', "Website Application"],
        ['mobileapp', "Mobile Application"]

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

    public generateDoc(card: Card) {
        let mapping = this.controller.getCardMappings(card.id);
        let links: { document: { doctype: string; id: string }; ltype: string }[] = [];
        let cre = mapping.owasp_cre?.owasp_asvs as [] || [];
        if (!cre) {
            throw Error("cre has not been defined.")
        }
        cre.forEach((cre) => links.push({
            "document": {
                "doctype": "CRE",
                "id": cre
            },
            "ltype": "Linked To"
        }));
        return {
            "doctype": "Tool",
            "id": 'https://cornucopia.owasp.org' + card.url,
            "name": CreController.editions.get(card.edition),
            "section": card.suitNameLocal,
            "description": card.desc,
            "sectionID": card.id,
            "hyperlink": 'https://cornucopia.owasp.org' + card.url,
            "links": links,
            "tags": ["Threat modeling", CreController.category.get(card.edition)],
            "tooltype": "Defensive"
        };
    }
}
