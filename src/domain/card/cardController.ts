import fs from 'fs'
import fm from "front-matter"
import type { Card } from './card';
import { FileSystemHelper } from '$lib/filesystem/fileSystemHelper';
import { order } from './order';
import { SuitController } from '../suit/suitController';
import type { Suit } from '../suit/suit';

export class CardController {

    private data: any;

    constructor(data: any) {
        this.data = data;
    }

    public getCardBySuitAndName(suit : string, card : string) : Card
    {
        let base : string = './data/cards/webapp-cards-2.00/';
        let path : string = base + suit + '/' + (card.length == 1 ? card : card) + '/technical-note.md'// '/explanation.md';
        let file = fs.readFileSync(path, 'utf8');
        let parsed = fm(file);

        let cardObject = {} as Card;
        cardObject.summary = parsed.body;
        cardObject.suit = suit;
        cardObject.suitName = (new SuitController(this.data)).getSuitNameByCardId(card);
        cardObject.card = card;
        cardObject.cardName = CardController.getCardNameById(card);
        cardObject.url = '/' + suit + '/' + card;
        cardObject.githubUrl = 'data/cards/webapp-cards-2.00/' + suit + '/' + card;

        return cardObject;
    }

    public static getCardNameById(id : string) : string
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

    public getCard(suit : string, card : string) : Card | undefined
    {
        suit = CardController.parseSuit(suit);

        for(let i = 0 ; i < this.data.suits.length ; i++)
        {
            if(this.data.suits[i].name.toLowerCase() == suit.toLowerCase())
            {
                for(let j = 0 ; j < this.data.suits[i].cards.length ; j++)
                {
                    if(this.data.suits[i].cards[j].id == card)
                    {
                        return this.data.suits[i].cards[j] as Card;
                    }
                }
            }
        }
    }

    private static parseSuit(suit : string) : string
    {
        suit = suit.replaceAll("-" , " ");
        return suit;

    }

    public getCardDescription(suit : string , card : string) : string
    {
        let thisCard : Card | undefined = this.getCard(suit,card);
        if(!thisCard)
            return "";

        return thisCard.desc
    }

    public getCardExplanation(suit : string , card : string) : string
    {
        let thisCard : Card | undefined = this.getCard(suit,card);
        if(!thisCard)
            return "";

        return thisCard.desc
    }

    public getCardImageUrl(suit : string , card : string, addition : number = 0) : string
    {
        if(!suit || !card)
            return "/cards/all/CORNUCOPIA.png";

        let thisCard : Card | undefined = this.getCard(suit,card);

        return '/cards/all/' + thisCard?.id + '.png';
    }

    public getCardsBySuit(suit : string) : Card[]
    {
        let base : string = './data/cards/webapp-cards-2.00/';
        let path : string = base + suit;
        let directories = FileSystemHelper.getDirectories(path);
        let cards = new Array<Card>();

        for(let i = 0 ; i < directories.length ; i++)
        {
            let name : string = directories[i];
            let card : Card = this.getCardBySuitAndName(suit,name);
            cards.push(card);
        }

        return cards.sort(CardController.orderFunction);
    }

    public getCardById(id : string) : Card
    {
        let suits : Suit[] = (new SuitController(this.data)).getSuits();
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
        cardObject.suitName = (new SuitController(this.data)).getSuitNameByCardId(cardObject.card);
        cardObject.url = '/' + suit + '/' + cardObject.card;
        cardObject.githubUrl = 'data/cards/webapp-cards-2.00/' + suit + '/' + cardObject.card;

        return cardObject;
    }

    public getCardsFlat() : Card[]
    {
        let result = new Array<Card>();
        let suits : Suit[] = (new SuitController(this.data)).getSuits();
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
        let orderA = order.get(a.card) || -1;
        let orderB = order.get(b.card) || -1;
        return orderA < orderB ? -1 : 1
    }

}