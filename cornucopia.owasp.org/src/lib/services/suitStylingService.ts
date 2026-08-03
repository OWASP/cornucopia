import { YamlDataLoader } from "$lib/services/yamlDataLoader";

export type SuitStyling = { tab: string; watermark: string; royal: string };

export class SuitStylingService {
    private static readonly loader = new YamlDataLoader<Record<string, SuitStyling>>('styling', 'suits', 'styling');

    public getSuitStyling(edition: string, version: string): Record<string, SuitStyling> | undefined {
        return SuitStylingService.loader.get(edition, version);
    }

    public static clear(): void {
        SuitStylingService.loader.clear();
    }
}
