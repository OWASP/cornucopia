import { DeckService } from "$lib/services/deckService";
import request from 'sync-request';
import {SuitController } from "../domain/suit/suitController";

export function load()
{
    return {
        suits : SuitController.getSuits(),
        cards: (new DeckService(request)).getCards('en'),
        mappingData: (new DeckService(request)).getCardMapping()
    }
}
