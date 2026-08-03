import fs from 'fs';
import * as yaml from "js-yaml";
import path from "path";
const __dirname = path.resolve(path.dirname(''));

export type SuitStyling = { tab: string; watermark: string; royal: string };

export class SuitStylingService {
    private static readonly path: string = '/../source/';
    private static cache: object[] = [];

    public getSuitStyling(edition: string, version: string): Record<string, SuitStyling> | undefined {
        const cached = SuitStylingService.cache.find((entry) => entry?.edition == edition && entry?.version == version);
        if (cached) return cached?.data;

        const file = `${__dirname}${SuitStylingService.path}${edition}-styling-${version}.yaml`;
        try {
            const yamlData = fs.readFileSync(file, 'utf8');
            const data = yaml.load(yamlData, { schema: yaml.FAILSAFE_SCHEMA }) as { suits: Record<string, SuitStyling> };
            SuitStylingService.cache.push({ edition: edition, version: version, data: data.suits });
            return data.suits;
        } catch (e) {
            console.error(`Failed to load styling for ${edition}-${version}:`, e);
            return undefined;
        }
    }

    public static clear(): void {
        SuitStylingService.cache = [];
    }
}
