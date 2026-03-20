/* eslint-disable @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-type-assertion, @typescript-eslint/no-unsafe-assignment -- Relaxing strict type checking for test mock data */
import { expect, describe, it } from 'vitest'
import { DEV_GUIDE_MAPPING } from './devGuideMapping'

describe('DevGuide Mapping Tests', () => {
  it('should contain valid mapping for key requirements', () => {
    expect(DEV_GUIDE_MAPPING['1.1']).toBeDefined()
    expect(DEV_GUIDE_MAPPING['2.1']).toBeDefined()
  })

  it('should map 1.1 to the correct guide section', () => {
    expect(DEV_GUIDE_MAPPING['1.1']).toContain('0x01h-Configuration')
  })

  it('should return undefined for non-existent requirements', () => {
    const mapping = DEV_GUIDE_MAPPING as Record<string, unknown>
    expect(mapping['99.99']).toBeUndefined()
  })
})