import { expect, describe, it } from 'vitest';
import { MappingController } from './mappingController';

function isRecord(obj: unknown): obj is Record<string, unknown> {
  return typeof obj === 'object' && obj !== null && !Array.isArray(obj);
}

function isWebAppMapping(obj: unknown): obj is { id: string; owasp_asvs: string[] } {
  if (!isRecord(obj)) return false;
  // Aliasing to camelCase to satisfy the linter
  const { id, owasp_asvs: owaspAsvs } = obj;
  return typeof id === 'string' && Array.isArray(owaspAsvs);
}

function isMetaResult(obj: unknown): obj is { version: string } {
  if (!isRecord(obj)) return false;
  return typeof obj.version === 'string';
}

describe('MappingController Unit Tests', () => {
  it('should return web app card mapping data', () => {
    const mockData = {
      suits: {
        testSuit: {
          cards: { 'webapp-1': { id: 'webapp-1', owasp_asvs: ['1.1', '1.2'], name: 'Test Card' } }
        }
      }
    };
    const controller = new MappingController(mockData);
    const result = controller.getWebAppCardMappings('webapp-1');
    
    expect(result).toBeDefined();
    if (!isWebAppMapping(result)) throw new Error('Result is not a valid web app mapping');
    
    expect(result.id).toBe('webapp-1');
    expect(result.owasp_asvs).toContain('1.1');
  });

  it('should return empty object for missing cards', () => {
    const controller = new MappingController({ suits: {} });
    const result = controller.getWebAppCardMappings('non-existent');
    if (!isRecord(result)) throw new Error('Result is not a record');
    expect(Object.keys(result)).toHaveLength(0);
  });

  it('should return meta information', () => {
    const controller = new MappingController({ meta: { version: '1.2.3' }, suits: {} });
    const meta = controller.getMeta();
    if (!isMetaResult(meta)) throw new Error('Meta is not valid');
    expect(meta.version).toBe('1.2.3');
  });
});