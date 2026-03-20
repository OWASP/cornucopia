import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { CapecService } from './capecService'
import type { CapecData } from './capecService'
import fs from 'node:fs'

vi.mock('node:fs')

describe('CapecService tests', () => {
  beforeEach(() => {
    CapecService.clear()
    vi.clearAllMocks()
  })

  afterEach(() => {
    CapecService.clear()
  })

  it('should load and return CAPEC data for webapp 3.0', () => {
    const mockData: CapecData = {
      1: { id: 1, name: 'Accessing Functionality Not Properly Constrained by ACLs', description: '', solutions: [], owasp_asvs: ['13.2.2'] }
    }
    vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify(mockData))
    const result = CapecService.getCapecData('webapp', '3.0')
    expect(result[1]).toBeDefined()
    expect(result[1].name).toBe('Accessing Functionality Not Properly Constrained by ACLs')
  })

  it('should return cached data on subsequent calls', () => {
    const mockData: CapecData = {
      1: { id: 1, name: 'Test', description: '', solutions: [], owasp_asvs: [] }
    }
    vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify(mockData))
    CapecService.getCapecData('webapp', '3.0')
    CapecService.getCapecData('webapp', '3.0')
    expect(fs.readFileSync).toHaveBeenCalledTimes(1)
  })

  it('should return empty object on file read error', () => {
    vi.mocked(fs.readFileSync).mockImplementation(() => { throw new Error('ERR') })
    const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
    const result = CapecService.getCapecData('webapp', '3.0')
    expect(result).toEqual({})
    expect(consoleErrorSpy).toHaveBeenCalled()
    consoleErrorSpy.mockRestore()
  })
})