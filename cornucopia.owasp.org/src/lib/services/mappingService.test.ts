import { expect, describe, it, vi } from 'vitest';
import { MappingService } from './mappingService';
import fs from 'node:fs';

vi.mock('node:fs');

describe('MappingService: Line 15 and Branches', () => {
    it('covers getCardMapping success, empty yaml, and error branches', () => {
        // Line 12 (File Missing Branch)
        vi.mocked(fs.existsSync).mockReturnValue(false);
        expect(MappingService.getCardMapping('webapp', '2.2')).toEqual({ suits: {} });

        //  TARGET: Line 15 Fallback (Forces yaml.load to return falsy)
        vi.mocked(fs.existsSync).mockReturnValue(true);
        vi.mocked(fs.readFileSync).mockReturnValue(''); 
        expect(MappingService.getCardMapping('webapp', '2.2')).toEqual({ suits: {} });

        // Line 14-15 (Success Branch)
        vi.mocked(fs.readFileSync).mockReturnValue('suits:\n  S1: Mapped');
        expect(MappingService.getCardMapping('webapp', '2.2')).toHaveProperty('suits');

        // Line 17 (Error Catch Branch)
        vi.mocked(fs.readFileSync).mockImplementationOnce(() => { throw new Error('Disk Error'); });
        expect(MappingService.getCardMapping('webapp', '2.2')).toEqual({ suits: {} });
    });

    it('covers version iteration maps', () => {
        vi.mocked(fs.existsSync).mockReturnValue(true);
        vi.mocked(fs.readFileSync).mockReturnValue('suits: {}');
        const service = new MappingService();
        expect(service.getCardMappingForLatestEdtions().size).toBe(3);
        expect(service.getCardMappingForAllVersions().size).toBe(3);
    });

    it('covers empty clear method', () => {
        MappingService.clear(); 
    });
});