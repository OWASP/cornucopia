/* eslint-disable @typescript-eslint/no-explicit-any -- Required for cross-app data compatibility */
import fs from 'node:fs'
import path from 'node:path'
import yaml from 'js-yaml'

const ROOT_DIR = process.cwd()

/* eslint-disable-next-line @typescript-eslint/no-extraneous-class -- Static utility for mappings */
export class MappingService {
  private static getFilePath(edition: string, version: string): string {
    const fileName = `${edition}-mapping-${version}.yaml`
    const possiblePaths = [
      path.join(ROOT_DIR, 'source', fileName),
      path.join(ROOT_DIR, '..', 'source', fileName)
    ]
    return possiblePaths.find((p) => fs.existsSync(p)) ?? ''
  }

  public static getCardMapping(edition: string, version: string): Record<string, any> {
    const filePath = MappingService.getFilePath(edition, version)
    if (filePath === '') return { suits: {} }
    try {
      const content = fs.readFileSync(filePath, 'utf8')
      // Removed 'as unknown' because the linter already identifies this as unknown
      const data = yaml.load(content, { schema: yaml.FAILSAFE_SCHEMA })
      
      // Explicit comparison (fixes 'strict-boolean-expressions')
      // This maintains the 'null' branch in your coverage tests
      if (data === null || typeof data === 'undefined') {
        return { suits: {} }
      }
      
      // Cast to the expected return type
      return data as Record<string, any>
    } catch {
      return { suits: {} }
    }
  }

  public static getCardMappingForLatestEdtions(): Map<string, any> {
    const mappings = new Map<string, any>()
    mappings.set('webapp-2.2', MappingService.getCardMapping('webapp', '2.2'))
    mappings.set('webapp-3.0', MappingService.getCardMapping('webapp', '3.0'))
    mappings.set('mobileapp-1.1', MappingService.getCardMapping('mobileapp', '1.1'))
    return mappings
  }

  public static getCardMappingForAllVersions(): Map<string, any> {
    return MappingService.getCardMappingForLatestEdtions()
  }

  public static clear(): void { /* No cache */ }
}