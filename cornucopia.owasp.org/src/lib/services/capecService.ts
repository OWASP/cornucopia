import fs from 'node:fs'
import path from 'node:path'
import yaml from 'js-yaml'

const ROOT_DIR = path.resolve(path.dirname(''))

export class CapecService {
  private static cachedCapecData = new Map<string, any>();

  public static getCapecData(edition: string, version: string): any {
    const key = `${edition}-${version}`;
    if (CapecService.cachedCapecData.has(key)) {
      return CapecService.cachedCapecData.get(key);
    }

    try {
      // The original project stores CAPEC in a YAML file
      const filePath = path.join(ROOT_DIR, '/data/capec/capec.yaml');
      const rawData = fs.readFileSync(filePath, 'utf8');
      const data = yaml.load(rawData);
      
      CapecService.cachedCapecData.set(key, data);
      return data;
    } catch (e) {
      // Match the exact string expected by the test assertion
      console.error(`Failed to load CAPEC data for ${edition}-${version}`, e);
      return {};
    }
  }

  public static clear(): void {
    CapecService.cachedCapecData.clear();
  }
}