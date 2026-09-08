import fs from 'fs';
import * as yaml from 'js-yaml';
import path from 'path';

const __dirname = path.resolve(path.dirname(''));

export type MasweData = Record<string, unknown>;

export class MasweService {
    private static masweData: Map<string, MasweData> = new Map();
    private static path = '/../source/';

    public static getMasweData(edition: string, version: string): MasweData {
        const key = `${edition}-${version}`;

        if (this.masweData.has(key)) {
            return this.masweData.get(key)!;
        }

        try {
            const yamlData = fs.readFileSync(
                `${__dirname}${this.path}${edition}-maswe-${version}.yaml`,
                'utf8'
            );
            const data = yaml.load(yamlData, { schema: yaml.FAILSAFE_SCHEMA }) as MasweData;
            this.masweData.set(key, data);
            return data;
        } catch (e) {
            console.error(`Failed to load MASWE data for ${edition}-${version}:`, e);
            return {};
        }
    }

    public static clear(): void {
        this.masweData.clear();
    }
}
