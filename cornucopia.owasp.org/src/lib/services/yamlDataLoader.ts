import fs from 'fs';
import * as yaml from "js-yaml";
import path from "path";
import { FileSystemHelper } from "$lib/filesystem/fileSystemHelper";
const __dirname = path.resolve(path.dirname(''));

type CacheEntry<T> = { edition: string; version: string; data: T };

// Shared by CardImagesService/SuitStylingService (and future per-edition yaml-backed data),
// each of which owns its own instance so their caches stay isolated.
export class YamlDataLoader<T> {
    private cache: CacheEntry<T>[] = [];

    constructor(
        private readonly fileSuffix: string,
        private readonly rootKey: string,
        private readonly errorLabel: string
    ) {}

    // Uses FAILSAFE_SCHEMA like the other loaders
    public get(edition: string, version: string): T | undefined {
        const cached = this.cache.find((entry) => entry.edition === edition && entry.version === version);
        if (cached) return cached.data;

        const file = `${__dirname}/../source/${edition}-${this.fileSuffix}-${version}.yaml`;
        // Not every edition has this data configured yet, so a missing file is expected, not an error
        if (!FileSystemHelper.hasFile(file)) return undefined;

        try {
            const yamlData = fs.readFileSync(file, 'utf8');
            const parsed = yaml.load(yamlData, { schema: yaml.FAILSAFE_SCHEMA }) as Record<string, T>;
            const data = parsed[this.rootKey];
            this.cache.push({ edition, version, data });
            return data;
        } catch (e) {
            console.error(`Failed to load ${this.errorLabel} for ${edition}-${version}:`, e);
            return undefined;
        }
    }

    public clear(): void {
        this.cache = [];
    }
}
