import type { Suit } from "./suit";
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { order } from "./order";

export class SuitController {

    private static decks = [{edition: 'mobileapp', version: '1.00'}, {edition: 'webapp', version: '2.00'}];

    public static getSuits() : Map<string,Suit[]>
    {
        let decks  : Map<string,Suit[]> = new Map<string,Suit[]>;
        SuitController.decks.forEach(deck => {
            let path : string = `./data/cards/${deck.edition}-cards-${deck.version}/`;
            let directories = FileSystemHelper.getDirectories(path);

            let suits = new Array<Suit>();

            for(let i = 0 ; i < directories.length ; i++)
            {
                let directory : string = directories[i];
                let suitPath : string = `./data/cards/${deck.edition}-cards-${deck.version}/${directory}`;
                let suitDirectories = FileSystemHelper.getDirectories(suitPath);
                let suit : Suit = 
                {
                    name : directory,
                    cards : suitDirectories.sort(SuitController.orderCards)
                };
                suits.push(suit);
            }
            decks.set(deck.edition, suits.sort(SuitController.orderFunction));
        });
        return decks;
    }

    public static orderFunction(a: Suit, b: Suit) : number
    {
        let orderA = order.get(a.name) || -1;
        let orderB = order.get(b.name) || -1;
        return orderA < orderB ? -1 : 1
    }

    public static orderCards(a: string, b: string) : number
    {
        let orderA = order.get(a) || -1;
        let orderB = order.get(b) || -1;
        return orderA < orderB ? -1 : 1
    }

}