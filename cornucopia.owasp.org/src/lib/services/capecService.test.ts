/* eslint-disable @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-explicit-any -- Required for Vitest mocks */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { CapecService } from './capecService';
import fs from 'node:fs';
import yaml from 'js-yaml';

vi.mock('node:fs');
vi.mock('js-yaml');

describe('CapecService: Global Suite', () => {
    beforeEach(() => {
        CapecService.clear();
        vi.clearAllMocks();
    });

    afterEach(() => {
        CapecService.clear();
    });

    it('should load and return CAPEC data for webapp 3.0', () => {
        const mockYamlContent = '1: { name: "test" }';
        const mockParsedData: any = {
            1: {
                name: 'Accessing Functionality Not Properly Constrained by ACLs',
                owasp_asvs: ['13.2.2', '13.3.2', '8.1.1']
            }
        };
        vi.mocked(fs.readFileSync).mockReturnValue(mockYamlContent);
        vi.mocked(yaml.load).mockReturnValue(mockParsedData);

        const result: any = CapecService.getCapecData('webapp', '3.0');
        expect(result[1].name).toBe('Accessing Functionality Not Properly Constrained by ACLs');
    });

    it('should return cached data on subsequent calls', () => {
        vi.mocked(fs.readFileSync).mockReturnValue('1: { name: "test" }');
        vi.mocked(yaml.load).mockReturnValue({ 1: { name: 'Test' } });
        CapecService.getCapecData('webapp', '3.0');
        CapecService.getCapecData('webapp', '3.0');
        expect(fs.readFileSync).toHaveBeenCalledTimes(1);
    });

    it('should return empty object on file read error', () => {
        vi.mocked(fs.readFileSync).mockImplementation(() => { throw new Error('File not found'); });
        const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
        expect(CapecService.getCapecData('webapp', '3.0')).toEqual({});
        consoleErrorSpy.mockRestore();
    });
});