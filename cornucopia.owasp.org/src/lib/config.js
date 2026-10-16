import * as yaml from 'js-yaml';
import yamlText from '../../decks.yaml?raw';

export const config = yamlText ? yaml.load(yamlText) : {};
export const decks =
    config !== null && typeof config === 'object' && 'decks' in config
        ? config.decks
        : undefined;
