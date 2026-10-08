import { describe, it, expect, vi } from 'vitest';

vi.mock('../../decks.yaml?raw', () => ({
    default: `
decks:
  - edition: webapp
    displayName: "OWASP Cornucopia"
    fullName: "Website App Edition"
    cre:
      name: "OWASP Cornucopia Website App Edition"
      category: "Website Application"
    defaultPreviewCard: VE2
    buttonLabelKey: cards.button.1
    descriptionHeadingKey: cards.h2.1
    descriptionBodyKey: cards.p2
    howToPlayLink: /how-to-play
    versions:
      - version: "2.2"
`
}));

describe('config.js', () => {
    it('getRawYaml returns a non-empty string', async () => {
        const { getRawYaml } = await import('./config.js');
        expect(typeof getRawYaml()).toBe('string');
        expect(getRawYaml().length).toBeGreaterThan(0);
    });

    it('config is a parsed object with a decks array', async () => {
        const { config } = await import('./config.js');
        expect(typeof config).toBe('object');
        expect(Array.isArray((config as any).decks)).toBe(true);
    });

    it('decks exposes config.decks', async () => {
        const { config, decks } = await import('./config.js');
        expect(decks).toBe((config as any).decks);
    });
});