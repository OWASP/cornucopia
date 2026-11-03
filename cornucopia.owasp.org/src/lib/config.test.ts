import { describe, it, expect, vi, beforeEach } from 'vitest';

const validYaml = `
decks:
  - edition: webapp
    displayName: "OWASP Cornucopia"
    versions:
      - version: "2.2"
`;

async function loadConfig(yamlText: string) {
    vi.resetModules();
    vi.doMock('../../application.yaml?raw', () => ({ default: yamlText }));
    return import('./config.js');
}

describe('config.js', () => {
    beforeEach(() => {
        vi.resetModules();
    });

    it('parses yaml into config and exposes decks', async () => {
        const { config, decks } = await loadConfig(validYaml);
        expect(Array.isArray(decks)).toBe(true);
        expect(decks).toHaveLength(1);
        expect((decks as any)[0].edition).toBe('webapp');
        expect(decks).toBe((config as any).decks);
    });

    it('returns empty config and undefined decks for empty yaml', async () => {
        const { config, decks } = await loadConfig('');
        expect(config).toEqual({});
        expect(decks).toBeUndefined();
    });

    it('returns undefined decks when the decks key is missing', async () => {
        const { decks } = await loadConfig('other: value');
        expect(decks).toBeUndefined();
    });

    it('returns undefined decks when yaml is not an object', async () => {
        const { decks } = await loadConfig('just a string');
        expect(decks).toBeUndefined();
    });

    it('returns undefined structuredData when structuredData key is missing', async () => {
        const { structuredData } = await loadConfig('other: value');
        expect(structuredData).toBeUndefined();
    });

    it('returns undefined structuredData when yaml is not an object', async () => {
        const { structuredData } = await loadConfig('just a string');
        expect(structuredData).toBeUndefined();
    });

    it('exposes structuredData when defined in yaml', async () => {
        const yamlWithData = `
decks: []
structuredData:
  website:
    name: "OWASP Cornucopia"
`;
        const { structuredData } = await loadConfig(yamlWithData);
        expect(structuredData).toEqual({
            website: { name: 'OWASP Cornucopia' },
        });
    });
});

