import fs from 'fs';
import * as yaml from "js-yaml";
import path from "path";
const __dirname = path.resolve(path.dirname(''));

export interface DeckVersionConfig {
    version: string;
    draftLanguages?: string[];
}

export interface DeckCre {
    name: string;
    category: string;
}

export interface DeckStandards {
    asvs?: { versionMap: Record<string, string> };
    capec?: { minVersion: string };
}

export interface DeckConfig {
    edition: string;
    displayName: string;
    fullName: string;
    cre: DeckCre;
    external?: boolean;
    standards?: DeckStandards;

    // required when external is false/absent - only browsable decks render on /cards and /edition/[edition]
    defaultPreviewCard?: string;
    buttonLabelKey?: string;
    descriptionHeadingKey?: string;
    descriptionBodyKey?: string;

    versions: DeckVersionConfig[];
}

interface DecksYaml {
    decks: DeckConfig[];
}

function collectDeckConfigErrors(deck: Partial<DeckConfig>, index: number): string[] {
    const errorLabel = deck.edition ? `deck "${deck.edition}"` : `decks[${index}]`;
    const errors: string[] = [];

    if (typeof deck.edition !== 'string' || !deck.edition) errors.push(`${errorLabel} is missing "edition"`);
    if (typeof deck.displayName !== 'string' || !deck.displayName) errors.push(`${errorLabel} is missing "displayName"`);
    if (typeof deck.fullName !== 'string' || !deck.fullName) errors.push(`${errorLabel} is missing "fullName"`);
    if (typeof deck.cre?.name !== 'string' || !deck.cre.name) errors.push(`${errorLabel} is missing "cre.name"`);
    if (typeof deck.cre?.category !== 'string' || !deck.cre.category) errors.push(`${errorLabel} is missing "cre.category"`);

    if (!Array.isArray(deck.versions)) {
        errors.push(`${errorLabel} is missing "versions" (must be an array, empty if fully drafted)`);
    } else {
        deck.versions.forEach((v, i) => {
            if (typeof v?.version !== 'string' || !v.version) {
                errors.push(`${errorLabel} versions[${i}] is missing "version"`);
            }
        });
    }

    if (!deck.external) {
        (['defaultPreviewCard', 'buttonLabelKey', 'descriptionHeadingKey', 'descriptionBodyKey'] as const).forEach((field) => {
            if (typeof deck[field] !== 'string' || !deck[field]) {
                errors.push(`${errorLabel} is not external but missing "${field}"`);
            }
        });
    }

    return errors;
}

function validateDecksYaml(decks: Partial<DeckConfig>[]): asserts decks is DeckConfig[] {
    const errors = decks.flatMap((deck, index) => collectDeckConfigErrors(deck, index));
    if (errors.length > 0) {
        throw new Error(`decks.yaml has ${errors.length} problem(s):\n` + errors.map((e) => `  - ${e}`).join('\n'));
    }
}


export class DeckConfigService {
    private static readonly path: string = '/decks.yaml';
    private static configs: DeckConfig[] | undefined;

    private static load(): DeckConfig[] {
        if (!DeckConfigService.configs) {
            const yamlData = fs.readFileSync(`${__dirname}${DeckConfigService.path}`, 'utf8');
            const parsed = yaml.load(yamlData) as DecksYaml;
            if (!Array.isArray(parsed?.decks)) throw new Error('decks.yaml: missing or invalid top-level "decks" array');
            validateDecksYaml(parsed.decks);
            DeckConfigService.configs = parsed.decks;
        }
        return DeckConfigService.configs;
    }

    public static getDeckConfigs(): DeckConfig[] {
        return DeckConfigService.load();
    }

    public static getDeckConfig(edition: string): DeckConfig | undefined {
        return DeckConfigService.load().find((deck) => deck.edition === edition);
    }

    // Non-external decks are the ones to be browsed on the site.
    public static getBrowsableDecks(): DeckConfig[] {
        return DeckConfigService.load().filter((deck) => !deck.external);
    }

    public static getPublishedVersions(edition: string): string[] {
        return DeckConfigService.getDeckConfig(edition)?.versions.map((v) => v.version) ?? [];
    }

    public static getDraftLanguages(edition: string, version: string): string[] {
        return DeckConfigService.getDeckConfig(edition)?.versions.find((v) => v.version === version)?.draftLanguages ?? [];
    }

    public static isExternal(edition: string): boolean {
        return DeckConfigService.getDeckConfig(edition)?.external ?? false;
    }

    public static getDisplayName(edition: string): string {
        return DeckConfigService.getDeckConfig(edition)?.displayName ?? edition;
    }

    public static getFullName(edition: string): string {
        return DeckConfigService.getDeckConfig(edition)?.fullName ?? edition;
    }

    public static getCreCategory(edition: string): string | undefined {
        return DeckConfigService.getDeckConfig(edition)?.cre.category;
    }

    public static getCreEditionName(edition: string): string | undefined {
        return DeckConfigService.getDeckConfig(edition)?.cre.name;
    }

    public static getAsvsVersion(edition: string, version: string): string {
        return DeckConfigService.getDeckConfig(edition)?.standards?.asvs?.versionMap[version] ?? '4.0.3';
    }

    public static hasCapecData(edition: string, version: string): boolean {
        const capec = DeckConfigService.getDeckConfig(edition)?.standards?.capec;
        return capec !== undefined && parseFloat(version) >= parseFloat(capec.minVersion);
    }

    public static clear(): void {
        DeckConfigService.configs = undefined;
    }
}
