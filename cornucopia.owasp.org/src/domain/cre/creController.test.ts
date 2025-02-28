import {expect, vi, describe, it} from 'vitest';
import { CreController } from './creController';
import yaml from "js-yaml";
import fs from "fs";

import { MappingController } from '../mapping/mappingController';

describe('CreController tests', () => {
    it("should return cre mapping data.", async () => {
        let mapping = yaml.load(fs.readFileSync("data/mock/mapping.yaml", 'utf8'));
        let cards = yaml.load(fs.readFileSync("data/mock/cards.yaml", 'utf8'));
        
        let controller = new MappingController(mapping);
        let creController = new CreController(cards, controller);
        expect(creController.getCreMapping()).toBeDefined();
    });
});