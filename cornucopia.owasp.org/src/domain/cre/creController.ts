import type { Card } from "../card/card";
import type { MappingController } from "../mapping/mappingController";
import { DeckConfigService } from "$lib/services/deckConfigService";

export type Cre =
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

    constructor(deck: Map<string, Card>, controller: MappingController) {
        this.deck = deck;
        this.controller = controller;
    }

    public static getEditionName(edition: string): string {
        return DeckConfigService.getCreEditionName(edition) ?? edition;
    }

    public getCreMapping(edition: string, lang: string) : any {
        if (!DeckConfigService.getDeckConfig(edition)) return {"meta": {}, "standards": []};
        const standards: Cre[] = [];
        (this.deck || []).forEach(
            (card: Card) => (card.edition == edition) && standards.push(this.generateDoc(card))
        );
        return {
            "meta": {
                "edition": CreController.getEditionName(edition),
                "component": 'cards',
                "language": lang,
                "version": this.controller.getMeta()?.version
            },
            "standards": standards
        };
    }

    public generateDoc(card: Card) {
        const mapping = this.controller.getCardMappings(card.id);
        const links: { document: { doctype: string; id: string }; ltype: string }[] = [];
        const cre = mapping.owasp_cre?.owasp_asvs as [] || [];
        const cardUrl = card.url.startsWith('http://') || card.url.startsWith('https://')
            ? card.url
            : 'https://cornucopia.owasp.org' + card.url;
        cre.forEach((cre) => links.push({
            "document": {
                "doctype": "CRE",
                "id": cre
            },
            "ltype": "Linked To"
        }));
        return {
            "doctype": "Tool",
            "id": cardUrl,
            "name": CreController.getEditionName(card.edition),
            "section": card.suitNameLocal,
            "description": card.desc,
            "sectionID": card.id,
            "hyperlink": cardUrl,
            "links": links,
            "tags": ["Threat modeling", DeckConfigService.getCreCategory(card.edition)],
            "tooltype": "Defensive"
        };
    }
}
