import fs from 'fs';
import yaml from "js-yaml";
import path from "path";

const __dirname = path.resolve(path.dirname(''));

export interface AsvsEntry {
    capec_codes: string[];
    description: string;
    level: string;
}

export interface AsvsData {
    [key: string]: AsvsEntry;
}

export class AsvsService {
    private static asvsData: Map<string, AsvsData> = new Map();
    private static path: string = '/../source/';

    public static getAsvsData(edition: string, version: string): AsvsData {
        const key = `${edition}-${version}`;

        if (this.asvsData.has(key)) {
            return this.asvsData.get(key)!;
        }

        try {
            const yamlData = fs.readFileSync(
                `${__dirname}${this.path}${edition}-asvs-${version}.yaml`,
                'utf8'
            );
            const data = yaml.load(yamlData, { schema: yaml.FAILSAFE_SCHEMA }) as AsvsData;
            this.asvsData.set(key, data);
            return data;
        } catch (e) {
            console.error(`Failed to load ASVS data for ${edition}-${version}:`, e);
            return {};
        }
    }

    public static clear(): void {
        this.asvsData.clear();
    }
}