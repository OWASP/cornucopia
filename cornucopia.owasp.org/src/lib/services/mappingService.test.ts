/* eslint-disable @typescript-eslint/no-unsafe-member-access -- Required for Vitest mock resolution */
import { describe, it, expect, vi } from 'vitest';
import { MappingService } from './mappingService';
import fs from 'node:fs';
import yaml from 'js-yaml';

describe('MappingService: Coverage Recovery', () => {
    it('covers all functions and branches', () => {
        // 1. Cover static 'clear' (Line 38)
        MappingService.clear();

        // 2. Cover 'getCardMapping' file missing branch (Line 13)
        vi.spyOn(fs, 'existsSync').mockReturnValue(false);
        expect(MappingService.getCardMapping('fake', '1.0').suits).toBeDefined();

        // 3. Cover 'getCardMapping' success branch (Lines 15-18)
        vi.spyOn(fs, 'existsSync').mockReturnValue(true);
        vi.spyOn(fs, 'readFileSync').mockReturnValue('suits: {}');
        vi.spyOn(yaml, 'load').mockReturnValue({ suits: { test: true } });
        expect(MappingService.getCardMapping('webapp', '2.2').suits.test).toBe(true);

        // 4. Cover 'getCardMapping' catch branch (Line 20)
        vi.spyOn(yaml, 'load').mockImplementation(() => { throw new Error('YAML Crash'); });
        expect(MappingService.getCardMapping('webapp', '2.2').suits).toBeDefined();

        // 5. Cover Instance methods for Routes (Lines 26-34)
        const service = new MappingService();
        const latest = service.getCardMappingForLatestEdtions();
        const all = service.getCardMappingForAllVersions();
        
        expect(latest instanceof Map).toBe(true);
        expect(all instanceof Map).toBe(true);

        vi.restoreAllMocks();
    });
});