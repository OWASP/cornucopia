import fs from 'node:fs'
import path from 'node:path'
import yaml from 'js-yaml'

const ROOT_DIR = path.resolve(path.dirname(''))

function isRecord(obj: unknown): obj is Record<string, unknown> {
  return typeof obj === 'object' && obj !== null && !Array.isArray(obj);
}

export class MappingService {
  private static readonly sourcePath = '/../source/'

  public static getCardMapping (edition: string, version: string): Record<string, unknown> {
    const filePath = path.join(ROOT_DIR, MappingService.sourcePath, `${edition}-mapping-${version}.yaml`)
    if (!fs.existsSync(filePath)) return { suits: {} }
    try {
      const content = fs.readFileSync(filePath, 'utf8')
      const result = yaml.load(content, { schema: yaml.FAILSAFE_SCHEMA })
      if (isRecord(result)) return result;
      return { suits: {} }
    } catch (e) {
      console.error('Mapping load error:', e)
      return { suits: {} }
    }
  }

  // eslint-disable-next-line @typescript-eslint/class-methods-use-this -- This method must be an instance method to avoid breaking existing calls in the routes and loaders.
  public getCardMappingForLatestEdtions (): Map<string, unknown> {
    const mappings = new Map<string, unknown>()
    for (const item of [{ e: 'webapp', v: '2.2' }, { e: 'mobileapp', v: '1.1' }]) {
      mappings.set(item.e, MappingService.getCardMapping(item.e, item.v))
    }
    return mappings
  }

  public getCardMappingForAllVersions (): Map<string, unknown> {
    return this.getCardMappingForLatestEdtions()
  }

  public static clear (): void {
    // No state to clear
  }
}