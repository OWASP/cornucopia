import fs from 'fs'
import fm from "front-matter"
import type { Card } from './card';
import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper';
import { order } from './order';
import { SuitController } from '../suit/suitController';
import type { Suit } from '../suit/suit';

export class CardController {

    private data: Card[];
    private edition: string;
    private version: string;

    constructor(data: Card[], edition:string, version:string) {
        this.data = data;
        
        this.edition = edition;
        this.version = version;
    }

    public getCardsBySuit(suit : string) : Card[]
    {
        let base : string = `./data/cards/${this.edition}-cards-${this.version}/`;
        let path : string = base + suit;
        let directories = FileSystemHelper.getDirectories(path);
        let cards = new Array<Card>();

        for(let i = 0 ; i < directories.length ; i++)
        {
            let name : string = directories[i];
            let card : Card = this.getCardById(name);
            cards.push(card);
        }

        return cards.sort(CardController.orderFunction);
    }

    public getCardById(id : string) : Card
    {
        return this.data.find((card) => card.id == id) as Card;
    }

    public getCardsFlat() : Card[]
    {
        let result = new Array<Card>();
        let suits : Suit[] = (new SuitController(this.data, this.edition, this.version)).getSuits();
        for(let i = 0 ; i < suits.length ; i++)
        {
            for(let j = 0 ; j < suits[i].cards.length ; j++)
            {
                let card : Card = suits[i].cards[j];
                result.push(card);
            }
        }
        return result;
    }

    public static orderFunction(a : Card, b : Card) : number
    {
        let orderA = order.get(a.id) || -1;
        let orderB = order.get(b.id) || -1;
        return orderA < orderB ? -1 : 1
    }

}