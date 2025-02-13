import type { Suit } from "./suit";
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
import { order } from "./order";
import { cardOrder } from "../card/order";
import lang from "$lib/translations/lang";

export class SuitController {

    private static decks = [{edition: 'mobileapp', version: '1.1'}, {edition: 'webapp', version: '2.1'}];
    private static languages : Map<string, any> = new Map<string, any>([
        ['mobileapp', {lang: ['en']}], 
        ['webapp', {lang: ['en', 'es', 'fr', 'nl', 'no_nb', 'pt_br']}]
    ]);

    public static getSuits() : Map<string,Suit[]>
    {
        let decks  : Map<string,Suit[]> = new Map<string,Suit[]>;
        SuitController.decks.forEach(deck => {
            let languages = SuitController.languages.get(deck.edition).lang;

            languages.forEach(lang => {

                let path : string = `./data/cards/${deck.edition}-cards-${deck.version}-${lang}/`;

                if(FileSystemHelper.hasDir(path)) {
                    let directories = FileSystemHelper.getDirectories(path);

                    let suits = new Array<Suit>();
    
                    for(let i = 0 ; i < directories.length ; i++)
                    {
                        let directory : string = directories[i];
                        let suitPath : string = `${path}/${directory}`;
                        let suitDirectories = FileSystemHelper.getDirectories(suitPath);
                        let suit : Suit = 
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
        let orderA = order.get(a.name) || -1;
        let orderB = order.get(b.name) || -1;
        return orderA < orderB ? -1 : 1
    }

    public static orderCards(a: string, b: string) : number
    {
        let orderA = cardOrder.get(a) || -1;
        let orderB = cardOrder.get(b) || -1;
        return orderA < orderB ? -1 : 1
    }

}