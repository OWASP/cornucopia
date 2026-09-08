import fs from 'fs';
import * as yaml from 'js-yaml';
import path from 'path';

const __dirname = path.resolve(path.dirname(''));

export type MastgData = Record<string, unknown>;

export class MastgService {
    private static mastgData: Map<string, MastgData> = new Map();
    private static path = '/../source/';

    public static getMastgData(edition: string, version: string): MastgData {
        const key = `${edition}-${version}`;

        if (this.mastgData.has(key)) {
            return this.mastgData.get(key)!;
        }

        try {
            const yamlData = fs.readFileSync(
                `${__dirname}${this.path}${edition}-mastg-${version}.yaml`,
                'utf8'
            );
            const data = yaml.load(yamlData, { schema: yaml.FAILSAFE_SCHEMA }) as MastgData;
            this.mastgData.set(key, data);
            return data;
        } catch (e) {
            console.error(`Failed to load MASTG data for ${edition}-${version}:`, e);
            return {};
        }
    }

    public static clear(): void {
        this.mastgData.clear();
    }
}
