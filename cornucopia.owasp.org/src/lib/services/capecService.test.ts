import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { CapecService } from './capecService';
import fs from 'fs';
import yaml from 'js-yaml';

vi.mock('fs');
vi.mock('js-yaml');

describe('CapecService tests', () => {
    beforeEach(() => {
        CapecService.clear();
        vi.clearAllMocks();
    });

    afterEach(() => {
        CapecService.clear();
    });

    describe('getCapecData', () => {
        it('should load and return CAPEC data for webapp 3.0', () => {
            const mockYamlContent = `
1:
  name: Accessing Functionality Not Properly Constrained by ACLs
  owasp_asvs:
    - 13.2.2
    - 13.3.2
    - 8.1.1
2:
  name: Inducing Account Lockout
  owasp_asvs:
    - 10.5.5
    - 2.3.2
`;

            const mockParsedData = {
                1: {
                    name: 'Accessing Functionality Not Properly Constrained by ACLs',
                    owasp_asvs: ['13.2.2', '13.3.2', '8.1.1']
                },
                2: {
                    name: 'Inducing Account Lockout',
                    owasp_asvs: ['10.5.5', '2.3.2']
                }
            };

            vi.mocked(fs.readFileSync).mockReturnValue(mockYamlContent);
            vi.mocked(yaml.load).mockReturnValue(mockParsedData);

            const result = CapecService.getCapecData('webapp', '3.0');

            expect(result).toBeDefined();
            expect(result[1]).toBeDefined();
            expect(result[1].name).toBe('Accessing Functionality Not Properly Constrained by ACLs');
            expect(result[1].owasp_asvs).toContain('13.2.2');
            expect(result[2]).toBeDefined();
            expect(result[2].name).toBe('Inducing Account Lockout');
        });

        it('should return cached data on subsequent calls', () => {
            const mockYamlContent = `
1:
  name: Test CAPEC
  owasp_asvs:
    - 1.1.1
`;

            const mockParsedData = {
                1: {
                    name: 'Test CAPEC',
                    owasp_asvs: ['1.1.1']
                }
            };

            vi.mocked(fs.readFileSync).mockReturnValue(mockYamlContent);
            vi.mocked(yaml.load).mockReturnValue(mockParsedData);

            // First call - should read file
            const result1 = CapecService.getCapecData('webapp', '3.0');
            expect(fs.readFileSync).toHaveBeenCalledTimes(1);

            // Second call - should use cache
            const result2 = CapecService.getCapecData('webapp', '3.0');
            expect(fs.readFileSync).toHaveBeenCalledTimes(1); // Still 1, not called again
            expect(result1).toBe(result2);
        });

        it('should handle different edition-version combinations separately', () => {
            const mockYamlContent1 = `
1:
  name: CAPEC 1
  owasp_asvs:
    - 1.1.1
`;

            const mockYamlContent2 = `
2:
  name: CAPEC 2
  owasp_asvs:
    - 2.2.2
`;

            const mockParsedData1 = {
                1: {
                    name: 'CAPEC 1',
                    owasp_asvs: ['1.1.1']
                }
            };

            const mockParsedData2 = {
                2: {
                    name: 'CAPEC 2',
                    owasp_asvs: ['2.2.2']
                }
            };

            vi.mocked(fs.readFileSync)
                .mockReturnValueOnce(mockYamlContent1)
                .mockReturnValueOnce(mockYamlContent2);
            
            vi.mocked(yaml.load)
                .mockReturnValueOnce(mockParsedData1)
                .mockReturnValueOnce(mockParsedData2);

            const result1 = CapecService.getCapecData('webapp', '3.0');
            const result2 = CapecService.getCapecData('webapp', '4.0');

            expect(result1[1]).toBeDefined();
            expect(result1[1].name).toBe('CAPEC 1');
            expect(result2[2]).toBeDefined();
            expect(result2[2].name).toBe('CAPEC 2');
        });

        it('should return empty object on file read error', () => {
            vi.mocked(fs.readFileSync).mockImplementation(() => {
                throw new Error('File not found');
            });

            const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

            const result = CapecService.getCapecData('webapp', '3.0');

            expect(result).toEqual({});
            expect(consoleErrorSpy).toHaveBeenCalledWith(
                expect.stringContaining('Failed to load CAPEC data for webapp-3.0'),
                expect.any(Error)
            );

            consoleErrorSpy.mockRestore();
        });

        it('should return empty object on YAML parse error', () => {
            vi.mocked(fs.readFileSync).mockReturnValue('invalid: yaml: content:');
            vi.mocked(yaml.load).mockImplementation(() => {
                throw new Error('YAML parse error');
            });

            const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

            const result = CapecService.getCapecData('webapp', '3.0');

            expect(result).toEqual({});
            expect(consoleErrorSpy).toHaveBeenCalled();

            consoleErrorSpy.mockRestore();
        });
    });

    describe('clear', () => {
        it('should clear the cache', () => {
            const mockYamlContent = `
1:
  name: Test
  owasp_asvs:
    - 1.1.1
`;

            const mockParsedData = {
                1: {
                    name: 'Test',
                    owasp_asvs: ['1.1.1']
                }
            };

            vi.mocked(fs.readFileSync).mockReturnValue(mockYamlContent);
            vi.mocked(yaml.load).mockReturnValue(mockParsedData);

            // Load data to populate cache
            CapecService.getCapecData('webapp', '3.0');
            expect(fs.readFileSync).toHaveBeenCalledTimes(1);

            // Clear cache
            CapecService.clear();

            // Load again - should read file again
            CapecService.getCapecData('webapp', '3.0');
            expect(fs.readFileSync).toHaveBeenCalledTimes(2);
        });
    });
});
