import attacks from '$lib/attacks.json'

export type Card = 
{
    id : string,
    desc : string,
}

export type Mapping = 
{
    id : string,
    owasp_scp : number[],
    owasp_asvs : string[],
    owasp_appsensor : string[],
    capec : number[],
    safecode : number[],

}

export function GetCard(suit : string, card : string) : Card | undefined
{
    suit = parseSuit(suit);

    for(let i = 0 ; i < data.suits.length ; i++)
    {
        if(data.suits[i].name.toLowerCase() == suit.toLowerCase())
        {
            for(let j = 0 ; j < data.suits[i].cards.length ; j++)
            {
                if(data.suits[i].cards[j].id == card)
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

export function GetCardMappings(suit : string, card : string, addition : number = 0) : Mapping | undefined
{
    suit = parseSuit(suit);

    for(let i = 0 ; i < mappings.suits.length ; i++)
    {
        if(mappings.suits[i].name.toLowerCase() == suit.toLowerCase())
        {
            for(let j = 0 ; j < mappings.suits[i].cards.length ; j++)
            {
                if(mappings.suits[i].cards[j].id == card)
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
        return "/cards/all/CORNUCOPIA.png";

    let thisCard : Card | undefined = GetCard(suit,card);

    return '/cards/all/' + thisCard?.id + '.png';
}

export type Attack = 
{
    name : string,
    url : string
}

export function GetCardAttacks(card : string) : Attack[]
{
    let id = card;
    let result : Attack[] = []

    for(let i = 0 ; i < attacks.list.length ; i++)
    {
        let attack = attacks.list[i];
        for(let j = 0 ; j < attack.cards.length ; j++)
        {
            let sampleID = attack.cards[j];
            if(id == sampleID)
            {
                result.push({name : attack.name,url : '../attacks/' + attack.url})
            }
        }
    }

    return result
}