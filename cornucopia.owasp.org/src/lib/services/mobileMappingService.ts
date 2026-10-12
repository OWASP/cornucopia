import fs from 'fs';
import * as yaml from 'js-yaml';
import path from 'path';

const __dirname = path.resolve(path.dirname(''));

export type MobileMappingComponent = 'mastg' | 'maswe';
export type MobileMappingData = Record<string, unknown>;

export class MobileMappingService {
    private readonly mappingData: Map<string, MobileMappingData> = new Map();
    private readonly path = '/../source/';

    public constructor(private readonly component: MobileMappingComponent) {}

    public getData(edition: string, version: string): MobileMappingData {
        const key = `${edition}-${version}`;

        if (this.mappingData.has(key)) {
            return this.mappingData.get(key)!;
        }

        try {
            const yamlData = fs.readFileSync(
                `${__dirname}${this.path}${edition}-${this.component}-${version}.yaml`,
                'utf8'
            );
            const data = yaml.load(yamlData, { schema: yaml.FAILSAFE_SCHEMA }) as MobileMappingData;
            this.mappingData.set(key, data);
            return data;
        } catch (e) {
            console.error(`Failed to load ${this.component.toUpperCase()} data for ${edition}-${version}:`, e);
            return {};
        }
    }

    public clear(): void {
        this.mappingData.clear();
    }
}
