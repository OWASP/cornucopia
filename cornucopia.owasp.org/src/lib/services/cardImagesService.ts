import fs from 'fs';
import * as yaml from "js-yaml";
import path from "path";
const __dirname = path.resolve(path.dirname(''));

export type CardImage = { image: string; opaque?: string };

export class CardImagesService {
    private static path: string = '/../source/';
    private static cache: object[] = [];

    // Uses FAILSAFE_SCHEMA like the other loaders
    public getCardImages(edition: string, version: string): Record<string, CardImage> | undefined {
        const cached = CardImagesService.cache.find((entry) => entry?.edition == edition && entry?.version == version);
        if (cached) return cached?.data;

        const file = `${__dirname}${CardImagesService.path}${edition}-card-images-${version}.yaml`;
        try {
            const yamlData = fs.readFileSync(file, 'utf8');
            const data = yaml.load(yamlData, { schema: yaml.FAILSAFE_SCHEMA }) as { cards: Record<string, CardImage> };
            CardImagesService.cache.push({ edition: edition, version: version, data: data.cards });
            return data.cards;
        } catch (e) {
            console.error(`Failed to load card images for ${edition}-${version}:`, e);
            return undefined;
        }
    }

    public static clear(): void {
        CardImagesService.cache = [];
    }
}
