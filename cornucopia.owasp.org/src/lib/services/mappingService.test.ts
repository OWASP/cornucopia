import {expect, describe, it} from 'vitest';
import { MappingService } from './mappingService';

describe('MappingService tests', () => {
    it("should return card mapping data.", async () => {
        expect((new MappingService()).getCardMappingForLatestEdtions()).toBeDefined();
        MappingService.clear();
        expect((new MappingService()).getCardMappingForAllVersions().get('webapp-2.2')).toBeDefined();
        expect((new MappingService()).getCardMappingForAllVersions().get('webapp-3.0')).toBeDefined();
        expect((new MappingService()).getCardMappingForAllVersions().get('mobileapp-1.1')).toBeDefined();
        MappingService.clear();

    });
});
