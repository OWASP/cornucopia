import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { MasweService } from './masweService';
import fs from 'fs';
import * as yaml from 'js-yaml';

vi.mock('fs');
vi.mock('js-yaml');

describe('MasweService tests', () => {
    beforeEach(() => {
        MasweService.clear();
        vi.clearAllMocks();
    });

    afterEach(() => {
        MasweService.clear();
    });

    it('loads and returns MASWE data', () => {
        const data = {
            meta: { component: 'maswe' },
            '0001': { owasp_mastg: ['0207'] }
        };
        vi.mocked(fs.readFileSync).mockReturnValue('maswe yaml');
        vi.mocked(yaml.load).mockReturnValue(data);

        expect(MasweService.getMasweData('mobileapp', '2.0')).toBe(data);
        expect(fs.readFileSync).toHaveBeenCalledWith(
            expect.stringContaining('mobileapp-maswe-2.0.yaml'),
            'utf8'
        );
    });

    it('returns cached data for the same edition and version', () => {
        const data = { '0001': { owasp_mastg: ['0207'] } };
        vi.mocked(fs.readFileSync).mockReturnValue('maswe yaml');
        vi.mocked(yaml.load).mockReturnValue(data);

        const first = MasweService.getMasweData('mobileapp', '2.0');
        const second = MasweService.getMasweData('mobileapp', '2.0');

        expect(first).toBe(second);
        expect(fs.readFileSync).toHaveBeenCalledTimes(1);
    });

    it('keeps different edition-version combinations separate', () => {
        const firstData = { '0001': { owasp_mastg: ['0207'] } };
        const secondData = { '0002': { owasp_mastg: ['0200'] } };
        vi.mocked(fs.readFileSync).mockReturnValueOnce('maswe yaml').mockReturnValueOnce('maswe yaml');
        vi.mocked(yaml.load).mockReturnValueOnce(firstData).mockReturnValueOnce(secondData);

        expect(MasweService.getMasweData('mobileapp', '2.0')).toBe(firstData);
        expect(MasweService.getMasweData('mobileapp', '3.0')).toBe(secondData);
        expect(fs.readFileSync).toHaveBeenCalledTimes(2);
    });

    it('returns an empty object when the file cannot be read', () => {
        vi.mocked(fs.readFileSync).mockImplementation(() => {
            throw new Error('File not found');
        });
        const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

        expect(MasweService.getMasweData('mobileapp', '2.0')).toEqual({});
        expect(consoleErrorSpy).toHaveBeenCalledWith(
            expect.stringContaining('Failed to load MASWE data for mobileapp-2.0'),
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

        expect(MasweService.getMasweData('mobileapp', '2.0')).toEqual({});
        expect(consoleErrorSpy).toHaveBeenCalled();

        consoleErrorSpy.mockRestore();
    });

    it('clears cached data', () => {
        vi.mocked(fs.readFileSync).mockReturnValue('maswe yaml');
        vi.mocked(yaml.load).mockReturnValue({ '0001': {} });

        MasweService.getMasweData('mobileapp', '2.0');
        MasweService.clear();
        MasweService.getMasweData('mobileapp', '2.0');

        expect(fs.readFileSync).toHaveBeenCalledTimes(2);
    });
});
