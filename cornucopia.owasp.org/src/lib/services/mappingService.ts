import fs from 'fs'
import yaml from "js-yaml";
import path from "path";
import { DeckService } from "$lib/services/deckService";
const __dirname = path.resolve(path.dirname(''));
export class MappingService {
    private static mappings: object[] = [];
    private static path: string = '/../source/';

    constructor() {
    }

    public getLatestsCardMappingData(edition: string)
    {
        const yamlData = fs.readFileSync(`${__dirname}${MappingService.path}${edition}-mappings-${DeckService.getLatestVersion(edition)}.yaml`, 'utf8');
        let data = yaml.load(yamlData);
        MappingService.mappings.push({edition: edition, version: 'latests', data: data});
        return data;
    }

    public getCardMapping(edition: string, version: string) : any
    {
        return this.getCardMappingForAllVersions().get(`${edition}-${version}`);
    }

    public getCardMappingDataAllVersions()
    {
        DeckService.getDecks().forEach((deck) => {
            const yamlData = fs.readFileSync(`${__dirname}${MappingService.path}${deck.edition}-mappings-${deck.version}.yaml`, 'utf8');
            let data = yaml.load(yamlData);
            MappingService.mappings.push({edition: deck.edition, version: deck.version, data: data});
        });
        
        return MappingService.mappings;
    }

    public getCardMappingForLatestEdtions() : Map<string, any>
    {
        const decks = new Map<string, any>();
        DeckService.getLatestEditions().forEach((edition) => {
            decks.set(
                edition, MappingService.mappings.find((mapping) => mapping?.version == 'latests' && mapping?.edition == edition)?.data || this.getLatestsCardMappingData(edition)
            );

            
        });
        return decks;
    }

    public getCardMappingForAllVersions() : Map<string, any>
    {
        const mapping = new Map<string, any>();
        
        // Load all mappings if not already loaded
        if (MappingService.mappings.length === 0) {
            this.getCardMappingDataAllVersions();
        }
        
        DeckService.getDecks().forEach((deck) => {
            let mappingData = MappingService.mappings.find((mapping) => mapping?.version == deck.version && mapping?.edition == deck.edition)?.data;
            
            // If not found in cache, try to load it
            if (!mappingData) {
                try {
                    const yamlData = fs.readFileSync(`${__dirname}${MappingService.path}${deck.edition}-mappings-${deck.version}.yaml`, 'utf8');
                    mappingData = yaml.load(yamlData);
                    MappingService.mappings.push({edition: deck.edition, version: deck.version, data: mappingData});
                } catch (e) {
                    console.error(`Failed to load mapping for ${deck.edition}-${deck.version}:`, e);
                }
            }
            
            if (mappingData) {
                mapping.set(`${deck.edition}-${deck.version}`, mappingData);
            }
        });
        return mapping;
    }

    public static clear(): void
    {
        MappingService.mappings = [];
    }
}