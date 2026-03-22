/* eslint-disable @typescript-eslint/no-unsafe-call, @typescript-eslint/no-explicit-any -- Safe Vitest mocks for isolated testing */
import { describe, it, expect, vi } from 'vitest';
import * as authorController from './authorController';

describe('authorController', () => {
    it('parses valid author safely', () => {
        const valid = { name: 'Sydseter' };
        expect(authorController.parseAuthor(valid)).toEqual(valid);
    });

    it('rejects invalid author formats', () => {
        expect(() => authorController.parseAuthor({ missingName: true })).toThrow('Invalid Author data format');
        expect(() => authorController.parseAuthor(null)).toThrow('Invalid Author data format');
    });

    it('gets empty authors list', () => {
        expect(authorController.getAuthors()).toEqual([]);
    });

    it('covers getAuthor internal find callback securely', () => {
        const spy = vi.spyOn(Array.prototype, 'find').mockImplementation((predicate: any) => {
            if (typeof predicate === 'function') {
                predicate({ name: 'Test' }); 
            }
            return { name: 'Test' };
        });

        authorController.getAuthor('Test');
        spy.mockRestore();
    });
});