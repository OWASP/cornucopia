import type { Suit } from "./suit";
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { getCardsBySuit } from "../card/cardController";
import data from "../../lib/data";
import { order } from "./order";

export function getSuits() : Suit[]
{
    let path : string = './data/cards/webapp-cards-1.22/';
    let directories = FileSystemHelper.getDirectories(path);

    let suits = new Array<Suit>();

    for(let i = 0 ; i < directories.length ; i++)
    {
        let directory : string = directories[i];
        let suit : Suit = 
        {
            name : directory,
            cards  : getCardsBySuit(directory)
        };
        suits.push(suit);
    }

    return suits.sort(orderFunction);
}

export function getSuitNameByCardId(id: string) : string
{
    const suit = data.suits.filter((suit) => {
        const card = suit.cards.filter(card => card.id == id)
        if (card != undefined && card.length > 0) return true;
        return false;
    })
    return suit[0]?.name;
}

function orderFunction(a : Suit, b : Suit) : number
{
    let orderA = order.get(a.name) || -1;
    let orderB = order.get(b.name) || -1;
    return orderA < orderB ? -1 : 1
}