import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { MastgService } from './mastgService';
import fs from 'fs';
import * as yaml from 'js-yaml';

vi.mock('fs');
vi.mock('js-yaml');

describe('MastgService tests', () => {
    beforeEach(() => {
        MastgService.clear();
        vi.clearAllMocks();
    });

    afterEach(() => {
        MastgService.clear();
    });

    it('loads and returns MASTG data', () => {
        const data = {
            meta: { component: 'mastg' },
            '0200': { owasp_maswe: ['0002'] }
        };
        vi.mocked(fs.readFileSync).mockReturnValue('mastg yaml');
        vi.mocked(yaml.load).mockReturnValue(data);

        expect(MastgService.getMastgData('mobileapp', '2.0')).toBe(data);
        expect(fs.readFileSync).toHaveBeenCalledWith(
            expect.stringContaining('mobileapp-mastg-2.0.yaml'),
            'utf8'
        );
    });

    it('returns cached data for the same edition and version', () => {
        const data = { '0200': { owasp_maswe: ['0002'] } };
        vi.mocked(fs.readFileSync).mockReturnValue('mastg yaml');
        vi.mocked(yaml.load).mockReturnValue(data);

        const first = MastgService.getMastgData('mobileapp', '2.0');
        const second = MastgService.getMastgData('mobileapp', '2.0');

        expect(first).toBe(second);
        expect(fs.readFileSync).toHaveBeenCalledTimes(1);
    });

    it('keeps different edition-version combinations separate', () => {
        const firstData = { '0200': { owasp_maswe: ['0002'] } };
        const secondData = { '0001': { owasp_mastg: ['0207'] } };
        vi.mocked(fs.readFileSync).mockReturnValueOnce('mastg yaml').mockReturnValueOnce('mastg yaml');
        vi.mocked(yaml.load).mockReturnValueOnce(firstData).mockReturnValueOnce(secondData);

        expect(MastgService.getMastgData('mobileapp', '2.0')).toBe(firstData);
        expect(MastgService.getMastgData('mobileapp', '3.0')).toBe(secondData);
        expect(fs.readFileSync).toHaveBeenCalledTimes(2);
    });

    it('returns an empty object when the file cannot be read', () => {
        vi.mocked(fs.readFileSync).mockImplementation(() => {
            throw new Error('File not found');
        });
        const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

        expect(MastgService.getMastgData('mobileapp', '2.0')).toEqual({});
        expect(consoleErrorSpy).toHaveBeenCalledWith(
            expect.stringContaining('Failed to load MASTG data for mobileapp-2.0'),
            expect.any(Error)
        );

        consoleErrorSpy.mockRestore();
    });

    it('returns an empty object when YAML parsing fails', () => {
        vi.mocked(fs.readFileSync).mockReturnValue('invalid yaml');
        vi.mocked(yaml.load).mockImplementation(() => {
            throw new Error('YAML parse error');
        });
        const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

        expect(MastgService.getMastgData('mobileapp', '2.0')).toEqual({});
        expect(consoleErrorSpy).toHaveBeenCalled();

        consoleErrorSpy.mockRestore();
    });

    it('clears cached data', () => {
        vi.mocked(fs.readFileSync).mockReturnValue('mastg yaml');
        vi.mocked(yaml.load).mockReturnValue({ '0200': {} });

        MastgService.getMastgData('mobileapp', '2.0');
        MastgService.clear();
        MastgService.getMastgData('mobileapp', '2.0');

        expect(fs.readFileSync).toHaveBeenCalledTimes(2);
    });
});
