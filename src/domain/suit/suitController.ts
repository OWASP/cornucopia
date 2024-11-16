import type { Suit } from "./suit";
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { CardController } from "../card/cardController";
import { order } from "./order";
import type { Card } from "../card/card";

export class SuitController {
    private data: Card[];
    private edition: string;
    private version: string;

    constructor(data: Card[], edition: string, version: string) {
        this.data = data;
        this.edition = edition;
        this.version = version;
    }

    public getSuits() : Suit[]
    {
        let path : string = `./data/cards/${this.edition}-cards-${this.version}/`;
        let directories = FileSystemHelper.getDirectories(path);

        let suits = new Array<Suit>();

        for(let i = 0 ; i < directories.length ; i++)
        {
            let directory : string = directories[i];
            let suit : Suit = 
            {
                name : directory,
                cards  : (new CardController(this.data, this.edition, this.version)).getCardsBySuit(directory)
            };
            suits.push(suit);
        }

        return suits.sort(SuitController.orderFunction);
    }

    public getSuitNameByCardId(id: string) : string
    {
        return this.data.find(card => card.id == id)?.suitName as string;
    }

    public static orderFunction(a : Suit, b : Suit) : number
    {
        let orderA = order.get(a.name) || -1;
        let orderB = order.get(b.name) || -1;
        return orderA < orderB ? -1 : 1
    }

}