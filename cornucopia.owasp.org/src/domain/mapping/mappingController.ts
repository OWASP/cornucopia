export type Mapping = Record<string, unknown> & {
    owasp_cre?: Record<string, unknown>;
    id?: string;
};

export type UrlTemplates = Record<string, string>;
export type MappingLabels = Record<string, string>;

function isRecord(value: unknown): value is Record<string, unknown> {
    return typeof value === "object" && value !== null && !Array.isArray(value);
}

export function getMappingUrl(
    urlTemplates: UrlTemplates,
    attribute: string | undefined,
    mapping: string | number,
): string | undefined {
    const template = attribute ? urlTemplates[attribute] : undefined;

    if (!template) return undefined;
    return template.includes("{code}")
        ? template.replaceAll("{code}", encodeURIComponent(String(mapping)))
        : template;
}

export function getMappingLabel(labels: MappingLabels, attribute: string): string | undefined {
    return labels[attribute];
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
    private mapping: Record<string, unknown>;

    constructor(mapping: Record<string, unknown>) {
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

    public getCardMappings(card : string, _addition : number = 0) : Mapping
    {
        const suits = this.mapping?.suits;
        if (!Array.isArray(suits)) {
            return {} as Mapping;
        }
        
        for (const suit of suits)
        {
            if (!isRecord(suit) || !Array.isArray(suit.cards)) continue;

            for (const cardMapping of suit.cards)
            {
                if (isRecord(cardMapping) && cardMapping.id === card)
                {
                    return cardMapping as Mapping;
                }
            }
        }
        return {} as Mapping;
    }

    public getMeta(): Record<string, unknown>
    {
        return isRecord(this.mapping?.meta) ? this.mapping.meta : {};
    }

    public getLabels(): MappingLabels
    {
        const labels = this.mapping?.labels;
        if (!labels || typeof labels !== "object" || Array.isArray(labels)) return {};

        return Object.fromEntries(
            Object.entries(labels).filter(
                (entry): entry is [string, string] => typeof entry[1] === "string"
            )
        );
    }

    public getUrlTemplates(): UrlTemplates
    {
        const urlTemplates = this.mapping?.url_templates;
        if (!urlTemplates || typeof urlTemplates !== "object" || Array.isArray(urlTemplates)) return {};

        return Object.fromEntries(
            Object.entries(urlTemplates).filter(
                (entry): entry is [string, string] => typeof entry[1] === "string"
            )
        );
    }

}
