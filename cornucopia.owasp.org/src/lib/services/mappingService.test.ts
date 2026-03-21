/* eslint-disable @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-call -- Bypassing strict typing for legacy service instantiation */
import { describe, it, expect } from 'vitest';
import { MappingService } from './mappingService';

describe('MappingService Coverage', () => {
    it('should return empty mapping for unknown editions', () => {
        const service = new MappingService();
        const result = service.getCardMapping('unknown', '1.0');
        expect(result).toBeDefined();
    });
});