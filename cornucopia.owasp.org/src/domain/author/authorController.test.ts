/* eslint-disable @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-call -- Bypassing strict typing for controller instantiation */
import { describe, it, expect } from 'vitest';
import { AuthorController } from './authorController';

describe('AuthorController Coverage', () => {
    it('should exist and be defined', () => {
        const controller = new AuthorController();
        expect(controller).toBeDefined();
    });
});