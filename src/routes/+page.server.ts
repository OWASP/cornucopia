import { DeckService } from "$lib/services/deckService";
import request from 'sync-request';
import {SuitController } from "../domain/suit/suitController";

export function load()
{
    return {
        suits : (new SuitController((new DeckService(request)).getCards('webapp', 'en'))).getSuits(),
        cardData: (new DeckService(request)).getCards('webapp', 'en'),
    }
}
