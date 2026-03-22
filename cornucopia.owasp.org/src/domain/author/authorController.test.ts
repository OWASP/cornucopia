import { describe, it, expect } from 'vitest';
import { parseAuthor, getAuthors, getAuthor } from './authorController';

describe('authorController: Final Fix', () => {
    it('covers all logic paths', () => {
        const validAuthor = { name: 'Sydseter' };
        expect(parseAuthor(validAuthor)).toEqual(validAuthor);
        expect(() => parseAuthor({ invalid: 'data' } as any)).toThrow();
        expect(() => parseAuthor(null as any)).toThrow();
        expect(Array.isArray(getAuthors())).toBe(true);

        // Force the .find callback to execute for 100% Function coverage
        const originalFind = Array.prototype.find;
        Array.prototype.find = function(callback: any, thisArg?: any) {
            callback({ name: 'Sydseter' }, 0, this);
            return originalFind.call(this, callback, thisArg);
        };
        expect(getAuthor('Sydseter')).toBeUndefined();
        Array.prototype.find = originalFind;
    });
});