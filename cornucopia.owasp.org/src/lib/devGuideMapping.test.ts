/* eslint-disable @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-type-assertion -- The test environment requires flexible object access to verify dynamic security keys without excessive type casting or rigid interfaces */
import { describe, it, expect } from 'vitest';
import { DevGuideMapping } from './devguideMapping';

describe('DevGuideMapping', () => {
  it('should have a mapping for 1.1', () => {
    expect(DevGuideMapping['1.1']).toContain('0x01h-Configuration');
  });

  it('should have a mapping for 2.1', () => {
    expect(DevGuideMapping['2.1']).toContain('0x02h-Authentication');
  });

  it('should return undefined for non-existent keys', () => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any -- Using any here to safely test the behavior of the mapping with invalid/non-existent keys
    expect((DevGuideMapping as any)['9.9']).toBeUndefined();
  });
});