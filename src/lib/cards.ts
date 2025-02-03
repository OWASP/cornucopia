import data from "./data";
import mappings from "./mappings";
import attacks from '$lib/attacks.json'

export type Card = 
{
    id : string,
    value : string,
    desc : string,
}

export type Mapping = 
{
    value : string,
    owasp_scp : number[],
    owasp_asvs : string[],
    owasp_appsensor : string[],
    capec : number[],
    safecode : number[],

}

export function GetCard(suit : string, card : string) : Card | undefined
{
    suit = parseSuit(suit);
    card = parseCard(card);

    for(let i = 0 ; i < data.suits.length ; i++)
    {
        if(data.suits[i].name.toLowerCase() == suit.toLowerCase())
        {
            for(let j = 0 ; j < data.suits[i].cards.length ; j++)
            {
                if(data.suits[i].cards[j].value.toLowerCase() == card.toLowerCase())
                {
                    return data.suits[i].cards[j] as Card;
                }
            }
        }
    }
}

function parseSuit(suit : string) : string
{
    suit = suit.replaceAll("-" , " ");
    return suit;

}

function parseCard(card : string) : string
{
    card = card.replaceAll("-a" , "A");
    card = card.replaceAll("-b" , "B");
    return card;
}

export function GetCardMappings(suit : string, card : string, addition : number = 0) : Mapping | undefined
{
    suit = parseSuit(suit);
    card = parseCard(card);

    for(let i = 0 ; i < mappings.suits.length ; i++)
    {
        if(mappings.suits[i].name.toLowerCase() == suit.toLowerCase())
        {
            for(let j = 0 ; j < mappings.suits[i].cards.length ; j++)
            {
                if(mappings.suits[i].cards[j].value.toLowerCase() == card.toLowerCase())
                {
                    return mappings.suits[i].cards[j] as Mapping;
                }
            }
        }
    }

    return undefined;
}

export function GetCardDescription(suit : string , card : string) : string
{
    let thisCard : Card | undefined = GetCard(suit,card);
    if(!thisCard)
        return "";

    return thisCard.desc
}

export function GetCardExplanation(suit : string , card : string) : string
{
    let thisCard : Card | undefined = GetCard(suit,card);
    if(!thisCard)
        return "";

    return thisCard.desc
}

export function GetCardImageUrl(suit : string , card : string, addition : number = 0) : string
{
    if(!suit || !card)
        return "/cards/all/1.png";

    let id : number = -1;
    // find the correct card
    let cid = '000';

    let thisCard : Card | undefined = GetCard(suit,card);
    if(thisCard)
        cid = thisCard.id;


    let s = cid.substring(0,2);
    let c = cid.substring(2,3);
    let sval = 0;
    let cval = 0;

    if(s == 'DV')
        sval = 0;
    if(s == 'AC')
        sval = 1;
    if(s == 'SM')
        sval = 2;
    if(s == 'AZ')
        sval = 3;
    if(s == 'CR')
        sval = 4;
    if(s == 'CO')
        sval = 5;
    if(s == 'JO')
        sval = 6;

    if(c == 'X')
        cval = 10;
    else if(c == 'J')
        cval = 11;
    else if(c == 'Q')
        cval = 12;
    else if(c == 'K')
        cval = 13;
    else if(c == 'A')
        cval = 14;
    else
        cval = parseInt(c);

    if(c == "A" && s == "JO")
        id = 79
    else if(c == "B" && s == "JO")
        id = 80
    else
        id = sval * 13 + cval - 1;


    id += addition;

    if(id == 0)
        id = 80;

    if(id == 81)
        id = 1

    if(suit == 'explanation')
        id = 81;
    

    return '/cards/all/' + id + '.png';
}

export type Attack = 
{
    name : string,
    url : string
}

export function GetCardAttacks(suit : string, card : string) : Attack[]
{
    let id = convertSuitAndCardToId(suit,card);
    let result : Attack[] = []

    for(let i = 0 ; i < attacks.list.length ; i++)
    {
        let attack = attacks.list[i];
        for(let j = 0 ; j < attack.cards.length ; j++)
        {
            let sampleID = attack.cards[j];
            if(id.toUpperCase() == sampleID.toUpperCase())
            {
                result.push({name : attack.name,url : '../attacks/' + attack.url})
            }
        }
    }

    return result
}

function convertSuitAndCardToId(suit : string,card : string)
{
    suit = suit.toLowerCase();
    card = card.toLowerCase();

    let firstPart : string = "";
    let secondPart : string = "";

    if(suit == 'cryptography')
        firstPart = 'CR';

    if(suit == 'data-validation-&-encoding')
        firstPart = 'DV';

    if(suit == 'authentication')
        firstPart = 'AC';

    if(suit == 'authorization')
        firstPart = 'AZ';

    if(suit == 'session-management')
        firstPart = 'SM';

    if(suit == 'cornucopia')
        firstPart = 'CO';

    secondPart = card.toUpperCase();

    return firstPart + secondPart;
}