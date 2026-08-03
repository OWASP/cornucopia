import { YamlDataLoader } from "$lib/services/yamlDataLoader";

export type CardImage = { image: string };

export class CardImagesService {
    private static readonly loader = new YamlDataLoader<Record<string, CardImage>>('card-images', 'cards', 'card images');

    public getCardImages(edition: string, version: string): Record<string, CardImage> | undefined {
        return CardImagesService.loader.get(edition, version);
    }

    public static clear(): void {
        CardImagesService.loader.clear();
    }
}
