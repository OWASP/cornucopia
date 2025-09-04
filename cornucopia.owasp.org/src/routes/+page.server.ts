import { DeckService } from "$lib/services/deckService";
import {SuitController } from "../domain/suit/suitController";

export function load()
{
    return {
        suits : SuitController.getSuits(),
        cards: (new DeckService()).getCards('en'),
        mappingData: (new DeckService()).getCardMapping()
    }
}
