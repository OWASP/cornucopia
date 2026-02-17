import {expect, describe, it} from 'vitest';
import { MappingService } from './mappingService';

describe('MappingService tests', () => {

    it("should return card mapping data.", async () => {
        expect((new MappingService()).getCardMappingForLatestEdtions()).toBeDefined();
        MappingService.clear();

        const all = (new MappingService()).getCardMappingForAllVersions();
        expect(all.get('webapp-2.2')).toBeDefined();
        expect(all.get('webapp-3.0')).toBeDefined();
        expect(all.get('mobileapp-1.1')).toBeDefined();

        MappingService.clear();
    });

    it("should return undefined for invalid mapping", () => {
        const service = new MappingService();
        const result = service.getCardMapping('invalid', '0.0');
        expect(result).toBeUndefined();
    });

    it("should clear mappings cache safely", () => {
        MappingService.clear();
        expect(true).toBe(true);
    });

});

