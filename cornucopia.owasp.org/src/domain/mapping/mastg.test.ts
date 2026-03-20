import { expect, describe, it } from 'vitest';
import { MASTG_TESTS_MAPPING } from './mastg';

describe('MASTG_TESTS_MAPPING tests', () => {
    it("should have correct mapping for known keys", () => {
        expect(MASTG_TESTS_MAPPING["TEST-0001"]).toBe("STORAGE");
        expect(MASTG_TESTS_MAPPING["TEST-0025"]).toBe("CODE");
        expect(MASTG_TESTS_MAPPING["TEST-0038"]).toBe("RESILIENCE");
        expect(MASTG_TESTS_MAPPING["TEST-00600"]).toBeUndefined();
    });
});