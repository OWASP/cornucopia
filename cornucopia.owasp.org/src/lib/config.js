import * as yaml from 'js-yaml';
import yamlText from '../../application.yaml?raw';

export const config = yamlText ? yaml.load(yamlText) : {};
export const decks =
    config !== null && typeof config === 'object' && 'decks' in config
        ? config.decks
        : undefined;
export const structuredData =
    config !== null && typeof config === 'object' && 'structuredData' in config
        ? config.structuredData
        : undefined;
