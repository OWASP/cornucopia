import fs from 'fs'
import fm from "front-matter"
import type { Card } from './card';
import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper';
import { order } from './order';
import { getSuitNameByCardId, getSuits } from '../suit/suitController';
import type { Suit } from '../suit/suit';

export function getCardBySuitAndName(suit : string, card : string) : Card
{
    let base : string = './data/cards/webapp-cards-1.22/';
    let path : string = base + suit + '/' + (card.length == 1 ? card : card) + '/technical-note.md'// '/explanation.md';
    let file = fs.readFileSync(path, 'utf8');
    let parsed = fm(file);

    let cardObject = {} as Card;
    cardObject.summary = parsed.body;
    cardObject.suit = suit;
    cardObject.suitName = getSuitNameByCardId(card);
    cardObject.card = card;
    cardObject.cardName = getCardNameById(card);
    cardObject.url = '/' + suit + '/' + card;
    cardObject.githubUrl = 'data/cards/webapp-cards-1.22/' + suit + '/' + card;

    return cardObject;
}

function getCardNameById(id : string) : string
{
    // Given the card id (e.g. AZ1, SMQ) return the card value (e.g. 1, Q) by stripping out the following parts:
    return id
        .replace('CORNUCOPIA','Explanation')
        .replace('CR','')
        .replace('C','')
        .replace('JO','')
        .replace('VE','')
        .replace('AT','')
        .replace('SM','')
        .replace('AZ','')
}

export function getCardsBySuit(suit : string) : Card[]
{
    let base : string = './data/cards/webapp-cards-1.22/';
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

export function getCardById(id : string) : Card
{
    let suits : Suit[] = getSuits();
    let cardObject = {} as Card;
    let suit : string = '';
    for(let i = 0 ; i < suits.length ; i++)
    {
        for(let j = 0 ; j < suits[i].cards.length ; j++)
        {
            let card : Card = suits[i].cards[j];
            if (card.card == String(id).toUpperCase())
                cardObject = card
                suit = suits[i].name;
                
        }
    }
    cardObject.suitName = getSuitNameByCardId(cardObject.card);
    cardObject.url = '/' + suit + '/' + cardObject.card;
    cardObject.githubUrl = 'data/cards/webapp-cards-1.22/' + suit + '/' + cardObject.card;

    return cardObject;
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
    let orderA = order.get(a.card) || -1;
    let orderB = order.get(b.card) || -1;
    return orderA < orderB ? -1 : 1
}