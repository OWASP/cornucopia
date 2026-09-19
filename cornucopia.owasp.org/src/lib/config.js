// src/lib/config.js
import * as yaml from 'js-yaml';
import yamlText from '../../decks.yaml?raw';

// For lazy consumers (e.g. deckConfigService) that need per-call parsing
export function getRawYaml() { return yamlText; }

// Pre-parsed exports for direct use in Svelte modules
export const config = yamlText ? yaml.load(yamlText) : {};
export const decks = config?.decks ?? [];
