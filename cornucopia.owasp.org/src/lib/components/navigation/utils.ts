export function AddLink(links: Link[], name : string, href : string)
{
    links.push({name:name,href:href}) ;
}

export type Link = 
{
    name : string,
    href : string
};
