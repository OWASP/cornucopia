import fs from 'node:fs'
import path from 'node:path'

const ROOT_DIR = path.resolve(path.dirname(''))
const CAPEC_PATH = '/data/capec/capec.json'

export interface CapecEntry {
  id: number
  name: string
  description: string
  solutions: string[]
  owasp_asvs: string[]
}

export type CapecData = Record<string, CapecEntry | undefined>

function isCapecData(data: unknown): data is CapecData {
  return typeof data === 'object' && data !== null && !Array.isArray(data);
}

let cachedCapecData: CapecData | null = null;

export const CapecService = {
  loadData(): CapecData {
    if (cachedCapecData !== null) return cachedCapecData;
    try {
      const rawData = fs.readFileSync(path.join(ROOT_DIR, CAPEC_PATH), 'utf8');
      // Added : unknown to fix the unsafe assignment rule
      const parsed: unknown = JSON.parse(rawData);
      
      if (isCapecData(parsed)) {
        cachedCapecData = parsed;
        return cachedCapecData;
      }
      return {};
    } catch (e) {
      console.error('Failed to load CAPEC data:', e);
      return {};
    }
  },

  getCapecData(edition: string, version: string): CapecData {
    if (cachedCapecData !== null) return cachedCapecData;
    console.log(`Loading CAPEC data for ${edition}-${version}`);
    return CapecService.loadData();
  },

  getCapecById(id: number): CapecEntry | undefined {
    return CapecService.loadData()[String(id)];
  },

  getCapecMappings(ids: number[]): CapecEntry[] {
    const data = CapecService.loadData();
    return ids.reduce<CapecEntry[]>((acc, id) => {
      // Destructuring dictionary access to fix prefer-destructuring error
      const { [String(id)]: entry } = data;
      if (entry !== undefined) {
        acc.push(entry);
      }
      return acc;
    }, []);
  },

  clear(): void {
    cachedCapecData = null;
  }
}