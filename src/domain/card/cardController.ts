import fs from 'fs'
import fm from "front-matter"
import type { Card } from './card';
import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper';
import { order } from './order';
import { getSuits } from '../suit/suitController';
import type { Suit } from '../suit/suit';

export function getCardBySuitAndName(suit : string, card : string) : Card
{
    let base : string = './data/cards/cornucopia-v1/';
    let path : string = base + suit + '/' + (card.length == 1 ? card.toUpperCase() : card) + '/technical-note.md'// '/explanation.md';
    let file = fs.readFileSync(path, 'utf8');
    let parsed = fm(file);

    let cardObject = {} as Card;
    cardObject.summary = parsed.body;
    cardObject.suit = suit;
    cardObject.card = card.toLowerCase();
    cardObject.url = '/' + suit + '/' + card.toLowerCase();
    cardObject.githubUrl = 'data/cards/cornucopia-v1/' + suit + '/' + card;

    return cardObject;
}

export function getCardsBySuit(suit : string) : Card[]
{
    let base : string = './data/cards/cornucopia-v1/';
    let path : string = base + suit;
    let directories = FileSystemHelper.getDirectories(path);
    let cards = new Array<Card>();

    for(let i = 0 ; i < directories.length ; i++)
    {
        let name : string = directories[i];
        let card : Card = getCardBySuitAndName(suit,name);
        cards.push(card);
    }

    return cards.sort(orderFunction);
}

export function getCardsFlat() : Card[]
{
    let result = new Array<Card>();
    let suits : Suit[] = getSuits();
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

function orderFunction(a : Card, b : Card) : number
{
    let orderA = order.get(a.card.toLowerCase()) || -1;
    let orderB = order.get(b.card.toLowerCase()) || -1;
    return orderA < orderB ? -1 : 1
}