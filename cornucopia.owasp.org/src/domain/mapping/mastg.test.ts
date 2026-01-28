import {expect, describe, it} from 'vitest';
import { MASTG_TESTS_MAPPING } from './mastg';

describe('MASTG_TESTS_MAPPING tests', () => {
    it("should have correct mapping for TEST-0001 to TEST-0059.", async () => {
        expect(MASTG_TESTS_MAPPING["TEST-0001"]).toBe("STORAGE"); 
        expect(MASTG_TESTS_MAPPING["TEST-0025"]).toBe("CODE");

        expect(MASTG_TESTS_MAPPING["TEST-0038"]).toBe("RESILIENCE");
        expect(MASTG_TESTS_MAPPING["TEST-0059"]).toBe("PLATFORM");
        expect(MASTG_TESTS_MAPPING["TEST-00600"]).toBeUndefined();
        expect(Object.keys(MASTG_TESTS_MAPPING).length).toBe(93); 
    });
});