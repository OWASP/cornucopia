import type { Suit } from "./suit";
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { order } from "./order";
import { cardOrder } from "$domain/card/order";

export class SuitController {

    private static decks = [{edition: 'mobileapp', version: '1.1'}, {edition: 'webapp', version: '2.2'}, {edition: 'companion', version: '1.0'}];
    private static languages : Map<string, { lang: string[] }> = new Map<string, { lang: string[] }>([
        ['mobileapp', {lang: ['en']}], 
        ['webapp', {lang: ['en', 'es', 'fr', 'nl', 'no_nb', 'pt_br', 'pt_pt', 'ru', 'it']}],
        ['companion', {lang: ['en']}]
    ]);

    public static getSuits() : Map<string,Suit[]>
    {
        const decks  : Map<string,Suit[]> = new Map<string,Suit[]>;
        SuitController.decks.forEach(deck => {
            const languages = SuitController.languages.get(deck.edition).lang;

            languages.forEach(lang => {

                const path : string = `./data/cards/${deck.edition}-cards-${deck.version}-${lang}/`;

                if(FileSystemHelper.hasDir(path)) {
                    const directories = FileSystemHelper.getDirectories(path);

                    const suits = new Array<Suit>();
    
                    for(let i = 0 ; i < directories.length ; i++)
                    {
                        const directory : string = directories[i];
                        const suitPath : string = `${path}/${directory}`;
                        const suitDirectories = FileSystemHelper.getDirectories(suitPath);
                        const suit : Suit = 
                        {
                            name : directory,
                            cards : suitDirectories.sort(SuitController.orderCards)
                        };
                        suits.push(suit);
                    }
                    decks.set(`${deck.edition}-${lang}`, suits.sort(SuitController.orderFunction));
                }
            });
        });
        return decks;
    }

    public static orderFunction(a: Suit, b: Suit) : number
    {
        const orderA = order.get(a.name) || -1;
        const orderB = order.get(b.name) || -1;
        return orderA < orderB ? -1 : 1
    }

    public static orderCards(a: string, b: string) : number
    {
        const orderA = cardOrder.get(a) || -1;
        const orderB = cardOrder.get(b) || -1;
        return orderA < orderB ? -1 : 1
    }

}
