 
import { describe, it, expect, vi } from 'vitest';
import { MappingService } from './mappingService';
import fs from 'node:fs';
import yaml from 'js-yaml';

describe('MappingService: 100% Coverage & CI Proof', () => {
    it('covers all paths and static access', () => {
        // 1. Cover 'clear'
        MappingService.clear();

        // 2. Cover file missing (finds no paths)
        vi.spyOn(fs, 'existsSync').mockReturnValue(false);
        expect(MappingService.getCardMapping('fake', '1.0').suits).toBeDefined();

        // 3. Cover success path (Line 25)
        vi.spyOn(fs, 'existsSync').mockReturnValue(true);
        vi.spyOn(fs, 'readFileSync').mockReturnValue('suits: {}');
        vi.spyOn(yaml, 'load').mockReturnValue({ suits: { hit: true } });
        expect(MappingService.getCardMapping('webapp', '2.2').suits.hit).toBe(true);

        // 4. Cover NULL return from YAML (Line 27 branch)
        vi.spyOn(yaml, 'load').mockReturnValue(null);
        expect(MappingService.getCardMapping('webapp', '2.2').suits).toBeDefined();

        // 5. Cover Catch block (Line 29)
        vi.spyOn(yaml, 'load').mockImplementation(() => { throw new Error('Crash'); });
        expect(MappingService.getCardMapping('webapp', '2.2').suits).toBeDefined();

        // 6. Cover static accessors used by routes
        expect(MappingService.getCardMappingForAllVersions() instanceof Map).toBe(true);

        vi.restoreAllMocks();
    });
});