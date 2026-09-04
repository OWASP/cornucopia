import type { Suit } from "./suit";
import type { Card } from "$domain/card/card";
import { DeckService } from "$lib/services/deckService";

export class SuitController {

    private static groupCardsBySuit(cards: Map<string, Card>): Suit[] {
        const suits: Suit[] = [];
        cards.forEach((card) => {
            const suit = suits.find((s) => s.name === card.suit);
            if (suit) {
                suit.cards.push(card.id);
            } else {
                suits.push({ name: card.suit, cards: [card.id] });
            }
        });
        return suits;
    }

    public static getSuits(): Map<string, Suit[]> {
        const decks = new Map<string, Suit[]>();
        const deckService = new DeckService();

        DeckService.getLatestEditions().forEach((edition) => {
            const version = DeckService.getLatestVersion(edition);

            DeckService.getLanguagesForEditionVersion(edition, version).forEach((lang) => {
                const cards = deckService.getCardDataForEditionVersionLang(edition, version, lang);
                if (cards.size === 0) return;

                decks.set(`${edition}-${lang}`, SuitController.groupCardsBySuit(cards));
            });
        });
        return decks;
    }

}
