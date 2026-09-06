import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { DeckConfigService } from './deckConfigService';
import fs from 'fs';

vi.mock('fs');

const MOCK_DECKS_YAML = `
decks:
  - edition: webapp
    displayName: "OWASP Cornucopia"
    fullName: "Website App Edition"
    cre:
      name: "OWASP Cornucopia Website App Edition"
      category: "Website Application"
    standards:
      asvs:
        versionMap:
          "2.2": "4.0.3"
          "3.0": "5.0"
      capec:
        minVersion: "3.0"
    defaultPreviewCard: VE2
    buttonLabelKey: cards.button.1
    descriptionHeadingKey: cards.h2.1
    descriptionBodyKey: cards.p2
    versions:
      - version: "2.2"
        draftLanguages: [hu]
      - version: "3.0"

  - edition: dbd
    displayName: "Cornucopia"
    fullName: "Digital Benefits Deck Edition"
    external: true
    cre:
      name: "Cornucopia Digital Benefits and Disbenefits Edition"
      category: "Digital Benefits and Disbenefits"
    versions: []
`;

describe('DeckConfigService tests', () => {
    beforeEach(() => {
        DeckConfigService.clear();
        vi.clearAllMocks();
        vi.mocked(fs.readFileSync).mockReturnValue(MOCK_DECKS_YAML);
    });

    afterEach(() => {
        DeckConfigService.clear();
    });

    describe('validation', () => {
        it('should throw when the top-level "decks" key is missing', () => {
            vi.mocked(fs.readFileSync).mockReturnValue('defaults:\n  foo: bar\n');
            expect(() => DeckConfigService.getDeckConfigs()).toThrow('missing or invalid top-level "decks" array');
        });

        it('should throw naming the edition when "displayName" is missing', () => {
            vi.mocked(fs.readFileSync).mockReturnValue(`
decks:
  - edition: webapp
    fullName: "Website App Edition"
    cre:
      name: "OWASP Cornucopia Website App Edition"
      category: "Website Application"
    versions:
      - version: "3.0"
`);
            expect(() => DeckConfigService.getDeckConfigs()).toThrow('deck "webapp" is missing "displayName"');
        });

        it('should throw naming the index when "edition" itself is missing', () => {
            vi.mocked(fs.readFileSync).mockReturnValue(`
decks:
  - displayName: "OWASP Cornucopia"
    fullName: "Website App Edition"
    cre:
      name: "OWASP Cornucopia Website App Edition"
      category: "Website Application"
    versions:
      - version: "3.0"
`);
            expect(() => DeckConfigService.getDeckConfigs()).toThrow('decks[0] is missing "edition"');
        });

        it('should throw when "fullName" is missing', () => {
            vi.mocked(fs.readFileSync).mockReturnValue(`
decks:
  - edition: webapp
    displayName: "OWASP Cornucopia"
    cre:
      name: "OWASP Cornucopia Website App Edition"
      category: "Website Application"
    versions:
      - version: "3.0"
`);
            expect(() => DeckConfigService.getDeckConfigs()).toThrow('deck "webapp" is missing "fullName"');
        });

        it('should throw when "cre.name" is missing', () => {
            vi.mocked(fs.readFileSync).mockReturnValue(`
decks:
  - edition: webapp
    displayName: "OWASP Cornucopia"
    fullName: "Website App Edition"
    cre:
      category: "Website Application"
    versions:
      - version: "3.0"
`);
            expect(() => DeckConfigService.getDeckConfigs()).toThrow('deck "webapp" is missing "cre.name"');
        });

        it('should throw when "cre.category" is missing', () => {
            vi.mocked(fs.readFileSync).mockReturnValue(`
decks:
  - edition: webapp
    displayName: "OWASP Cornucopia"
    fullName: "Website App Edition"
    cre:
      name: "OWASP Cornucopia Website App Edition"
    versions:
      - version: "3.0"
`);
            expect(() => DeckConfigService.getDeckConfigs()).toThrow('deck "webapp" is missing "cre.category"');
        });

        it('should throw when "versions" is not an array', () => {
            vi.mocked(fs.readFileSync).mockReturnValue(`
decks:
  - edition: webapp
    displayName: "OWASP Cornucopia"
    fullName: "Website App Edition"
    cre:
      name: "OWASP Cornucopia Website App Edition"
      category: "Website Application"
`);
            expect(() => DeckConfigService.getDeckConfigs()).toThrow('deck "webapp" is missing "versions"');
        });

        it('should throw naming the version index when a versions entry is missing "version"', () => {
            vi.mocked(fs.readFileSync).mockReturnValue(`
decks:
  - edition: webapp
    displayName: "OWASP Cornucopia"
    fullName: "Website App Edition"
    cre:
      name: "OWASP Cornucopia Website App Edition"
      category: "Website Application"
    versions:
      - draftLanguages: [hu]
`);
            expect(() => DeckConfigService.getDeckConfigs()).toThrow('deck "webapp" versions[0] is missing "version"');
        });

        it('should accept an empty versions array (fully-drafted deck)', () => {
            vi.mocked(fs.readFileSync).mockReturnValue(`
decks:
  - edition: dbd
    displayName: "Cornucopia"
    fullName: "Digital Benefits Deck Edition"
    external: true
    cre:
      name: "Cornucopia Digital Benefits and Disbenefits Edition"
      category: "Digital Benefits and Disbenefits"
    versions: []
`);
            expect(() => DeckConfigService.getDeckConfigs()).not.toThrow();
        });

        it.each(['defaultPreviewCard', 'buttonLabelKey', 'descriptionHeadingKey', 'descriptionBodyKey'] as const)(
            'should throw when a non-external deck is missing "%s"',
            (missingField) => {
                const renderFields: Record<string, string> = {
                    defaultPreviewCard: 'VE2',
                    buttonLabelKey: 'cards.button.1',
                    descriptionHeadingKey: 'cards.h2.1',
                    descriptionBodyKey: 'cards.p2'
                };
                delete renderFields[missingField];
                const renderFieldsYaml = Object.entries(renderFields)
                    .map(([key, value]) => `    ${key}: ${value}`)
                    .join('\n');

                vi.mocked(fs.readFileSync).mockReturnValue(`
decks:
  - edition: webapp
    displayName: "OWASP Cornucopia"
    fullName: "Website App Edition"
    cre:
      name: "OWASP Cornucopia Website App Edition"
      category: "Website Application"
${renderFieldsYaml}
    versions:
      - version: "3.0"
`);
                expect(() => DeckConfigService.getDeckConfigs())
                    .toThrow(`deck "webapp" is not external but missing "${missingField}"`);
            }
        );

        it('should collect and report every problem across every deck, not just the first', () => {
            vi.mocked(fs.readFileSync).mockReturnValue(`
decks:
  - edition: webapp
    fullName: "Website App Edition"
    cre:
      name: "OWASP Cornucopia Website App Edition"
      category: "Website Application"
    defaultPreviewCard: VE2
    buttonLabelKey: cards.button.1
    descriptionHeadingKey: cards.h2.1
    descriptionBodyKey: cards.p2
    versions:
      - version: "3.0"

  - edition: dbd
    displayName: "Cornucopia"
    fullName: "Digital Benefits Deck Edition"
    external: true
    cre:
      name: "Cornucopia Digital Benefits and Disbenefits Edition"
    versions: []
`);
            let thrown: Error | undefined;
            try {
                DeckConfigService.getDeckConfigs();
            } catch (e) {
                thrown = e as Error;
            }

            expect(thrown).toBeDefined();
            expect(thrown?.message).toContain('deck "webapp" is missing "displayName"');
            expect(thrown?.message).toContain('deck "dbd" is missing "cre.category"');
            expect(thrown?.message).toContain('has 2 problem(s)');
        });
    });

    describe('getDeckConfigs', () => {
        it('should parse every deck entry from decks.yaml', () => {
            const configs = DeckConfigService.getDeckConfigs();
            expect(configs).toHaveLength(2);
            expect(configs.map((c) => c.edition)).toEqual(['webapp', 'dbd']);
        });

        it('should only read the file once and cache the result', () => {
            DeckConfigService.getDeckConfigs();
            DeckConfigService.getDeckConfigs();
            expect(fs.readFileSync).toHaveBeenCalledTimes(1);
        });
    });

    describe('getDeckConfig', () => {
        it('should return the config for a known edition', () => {
            expect(DeckConfigService.getDeckConfig('webapp')?.fullName).toBe('Website App Edition');
        });

        it('should return undefined for an unknown edition', () => {
            expect(DeckConfigService.getDeckConfig('unknown')).toBeUndefined();
        });
    });

    describe('getBrowsableDecks', () => {
        it('should exclude decks marked external', () => {
            const editions = DeckConfigService.getBrowsableDecks().map((d) => d.edition);
            expect(editions).toEqual(['webapp']);
        });
    });

    describe('getPublishedVersions', () => {
        it('should return every version listed for an edition, in file order', () => {
            expect(DeckConfigService.getPublishedVersions('webapp')).toEqual(['2.2', '3.0']);
        });

        it('should return an empty array for a fully-draft edition (versions: [])', () => {
            expect(DeckConfigService.getPublishedVersions('dbd')).toEqual([]);
        });

        it('should return an empty array for an unknown edition', () => {
            expect(DeckConfigService.getPublishedVersions('unknown')).toEqual([]);
        });
    });

    describe('getDraftLanguages', () => {
        it('should return the draftLanguages list for a version that has one', () => {
            expect(DeckConfigService.getDraftLanguages('webapp', '2.2')).toEqual(['hu']);
        });

        it('should return an empty array for a version without draftLanguages', () => {
            expect(DeckConfigService.getDraftLanguages('webapp', '3.0')).toEqual([]);
        });

        it('should return an empty array for an unpublished version', () => {
            expect(DeckConfigService.getDraftLanguages('webapp', '1.0')).toEqual([]);
        });
    });

    describe('isExternal', () => {
        it('should return true for a deck marked external', () => {
            expect(DeckConfigService.isExternal('dbd')).toBe(true);
        });

        it('should return false for a deck without the external flag', () => {
            expect(DeckConfigService.isExternal('webapp')).toBe(false);
        });

        it('should return false for an unknown edition', () => {
            expect(DeckConfigService.isExternal('unknown')).toBe(false);
        });
    });

    describe('name/category accessors', () => {
        it('should return displayName, falling back to the edition string', () => {
            expect(DeckConfigService.getDisplayName('webapp')).toBe('OWASP Cornucopia');
            expect(DeckConfigService.getDisplayName('unknown')).toBe('unknown');
        });

        it('should return fullName, falling back to the edition string', () => {
            expect(DeckConfigService.getFullName('dbd')).toBe('Digital Benefits Deck Edition');
            expect(DeckConfigService.getFullName('unknown')).toBe('unknown');
        });

        it('should return cre.category, or undefined when unknown', () => {
            expect(DeckConfigService.getCreCategory('dbd')).toBe('Digital Benefits and Disbenefits');
            expect(DeckConfigService.getCreCategory('unknown')).toBeUndefined();
        });

        it('should return cre.name, or undefined when unknown', () => {
            expect(DeckConfigService.getCreEditionName('webapp')).toBe('OWASP Cornucopia Website App Edition');
            expect(DeckConfigService.getCreEditionName('unknown')).toBeUndefined();
        });
    });

    describe('getAsvsVersion', () => {
        it('should look up the version from standards.asvs.versionMap', () => {
            expect(DeckConfigService.getAsvsVersion('webapp', '2.2')).toBe('4.0.3');
            expect(DeckConfigService.getAsvsVersion('webapp', '3.0')).toBe('5.0');
        });

        it('should fall back to 4.0.3 for a version not in the map', () => {
            expect(DeckConfigService.getAsvsVersion('webapp', '1.0')).toBe('4.0.3');
        });

        it('should fall back to 4.0.3 for an edition without a standards.asvs block', () => {
            expect(DeckConfigService.getAsvsVersion('dbd', '1.0')).toBe('4.0.3');
        });
    });

    describe('hasCapecData', () => {
        it('should return true at or above the configured minVersion', () => {
            expect(DeckConfigService.hasCapecData('webapp', '3.0')).toBe(true);
        });

        it('should return false below the configured minVersion', () => {
            expect(DeckConfigService.hasCapecData('webapp', '2.2')).toBe(false);
        });

        it('should return false for an edition without a standards.capec block', () => {
            expect(DeckConfigService.hasCapecData('dbd', '1.0')).toBe(false);
        });
    });

    describe('clear', () => {
        it('should force decks.yaml to be re-read on the next access', () => {
            DeckConfigService.getDeckConfigs();
            expect(fs.readFileSync).toHaveBeenCalledTimes(1);

            DeckConfigService.clear();
            DeckConfigService.getDeckConfigs();

            expect(fs.readFileSync).toHaveBeenCalledTimes(2);
        });
    });
});
