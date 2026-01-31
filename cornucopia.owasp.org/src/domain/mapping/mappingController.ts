export type Mapping  = 
{
    owasp_cre: any;
    id : string

}


export type WebAppMapping  = 
{
    id : string,
    owasp_dev_guide : number[],
    stride : string[],
    owasp_asvs : string[],
    owasp_appsensor : string[],
    capec : number[],
    safecode : number[],
    capec_map : {
    [key: number]: {
        owasp_asvs: (string)[],
        name: string,
        id: number
        }
    };

}

export type MobileAppMapping = 
{
    id : string,
    owasp_masvs : string[],
    owasp_mastg : string[],
    capec : number[],
    safecode : number[],
}

export class MappingController {
    private mapping: any;

    constructor(mapping: any) {
        this.mapping = mapping;
    }

    public getWebAppCardMappings(card : string) : WebAppMapping
    {
        return this.getCardMappings(card) as WebAppMapping;
    }

    public getMobileAppCardMappings(card : string) : MobileAppMapping
    {
        return this.getCardMappings(card) as MobileAppMapping;
    }

    public getCardMappings(card : string, addition : number = 0) : Mapping
    {
        if (!this.mapping || !this.mapping.suits) {
            return {} as Mapping;
        }
        
        for(let i = 0 ; i < this.mapping.suits.length ; i++)
        {
            for(let j = 0 ; j < this.mapping.suits[i].cards.length ; j++)
            {
                if(this.mapping.suits[i].cards[j].id == card)
                {
                    return this.mapping.suits[i].cards[j] as Mapping;
                }
            }
        }
        return {} as Mapping;
    }

    public getMeta() : any
    {
        return this.mapping?.meta;
    }

}