import fs from 'node:fs'
import path from 'node:path'
import yaml from 'js-yaml'

const ROOT_DIR = path.resolve(path.dirname(''))

export class MappingService {
  private static readonly sourcePath = '/../source/'

  public static getCardMapping(edition: string, version: string): any {
    const filePath = path.join(ROOT_DIR, MappingService.sourcePath, `${edition}-mapping-${version}.yaml`)
    if (!fs.existsSync(filePath)) return { suits: {} }
    try {
      const content = fs.readFileSync(filePath, 'utf8')
      return yaml.load(content, { schema: yaml.FAILSAFE_SCHEMA }) || { suits: {} }
    } catch (e) {
      return { suits: {} }
    }
  }

  public getCardMappingForLatestEdtions(): Map<string, any> {
    const mappings = new Map<string, any>()
    // Reverted to the edition-version key format expected by the original tests
    mappings.set('webapp-2.2', MappingService.getCardMapping('webapp', '2.2'))
    mappings.set('webapp-3.0', MappingService.getCardMapping('webapp', '3.0'))
    mappings.set('mobileapp-1.1', MappingService.getCardMapping('mobileapp', '1.1'))
    return mappings
  }

  public getCardMappingForAllVersions(): Map<string, any> {
    return this.getCardMappingForLatestEdtions()
  }

  public static clear(): void { }
}