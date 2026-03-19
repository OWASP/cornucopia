import fs from 'fs';
import yaml from "js-yaml";
import path from "path";

const __dirname = path.resolve(path.dirname(''));

export interface CapecData {
    [key: number]: {
        name: string;
        owasp_asvs: string[];
    };
}

export class CapecService {
    private static capecData: Map<string, CapecData> = new Map();
    private static path: string = '/../source/';

    public static getCapecData(edition: string, version: string): CapecData {
        const key = `${edition}-${version}`;
        
        if (this.capecData.has(key)) {
            return this.capecData.get(key)!;
        }

        try {
            const yamlData = fs.readFileSync(
                `${__dirname}${this.path}${edition}-capec-${version}.yaml`, 
                'utf8'
            );
            const data = yaml.load(yamlData, { schema: yaml.FAILSAFE_SCHEMA }) as CapecData;
            this.capecData.set(key, data);
            return data;
        } catch (e) {
            console.error(`Failed to load CAPEC data for ${edition}-${version}:`, e);
            return {};
        }
    }

    public static clear(): void {
        this.capecData.clear();
    }
}
