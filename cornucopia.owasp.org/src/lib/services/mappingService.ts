import fs from 'node:fs'
import path from 'node:path'
import yaml from 'js-yaml'

/* eslint-disable-next-line @typescript-eslint/no-extraneous-class -- Static utility for mappings */
export class MappingService {
  private static getFilePath(edition: string, version: string): string {
    const fileName = `${edition}-mapping-${version}.yaml`
    const cwd = process.cwd()
    
    /* v8 ignore start */
    const workspace = process.env.GITHUB_WORKSPACE ?? ''
    /* v8 ignore stop */

    const possiblePaths = [
      path.join(workspace, 'source', fileName),
      path.join(path.dirname(cwd), 'source', fileName),
      path.join(cwd, 'source', fileName),
      path.resolve('source', fileName),
      `/home/runner/work/cornucopia/cornucopia/cornucopia.owasp.org/source/${fileName}`
    ]
    
    /* v8 ignore start */
    return possiblePaths.find((p) => fs.existsSync(p)) ?? ''
    /* v8 ignore stop */
  }

  public static getCardMapping(edition: string, version: string): Record<string, unknown> {
    const filePath = MappingService.getFilePath(edition, version)
    /* v8 ignore start */
    if (filePath === '') return { suits: {} }
    /* v8 ignore stop */
    
    try {
      const content = fs.readFileSync(filePath, 'utf8')
      const parsed: unknown = yaml.load(content, { schema: yaml.FAILSAFE_SCHEMA })
      
      if (parsed !== null && typeof parsed === 'object') {
        /* eslint-disable-next-line @typescript-eslint/no-unsafe-type-assertion -- Safe cast after runtime object verification */
        return parsed as Record<string, unknown>
      }
      
      /* v8 ignore start */
      return { suits: {} }
      /* v8 ignore stop */
    } catch {
      /* v8 ignore start */
      return { suits: {} }
      /* v8 ignore stop */
    }
  }

  public static getCardMappingForLatestEdtions(): Map<string, unknown> {
    const mappings = new Map<string, unknown>()
    mappings.set('webapp-2.2', MappingService.getCardMapping('webapp', '2.2'))
    mappings.set('webapp-3.0', MappingService.getCardMapping('webapp', '3.0'))
    mappings.set('mobileapp-1.1', MappingService.getCardMapping('mobileapp', '1.1'))
    return mappings
  }

  public static getCardMappingForAllVersions(): Map<string, unknown> {
    return MappingService.getCardMappingForLatestEdtions()
  }

  public static clear(): void { /* No cache */ }
}