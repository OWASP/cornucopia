import { expect, describe, it } from 'vitest'
import { MappingService } from './mappingService'

describe('MappingService Unit Tests', () => {
  it('should return card mapping data for latest editions', () => {
    const service = new MappingService()
    const mapping = service.getCardMappingForLatestEdtions()
    expect(mapping).toBeDefined()
    MappingService.clear()
  })
})