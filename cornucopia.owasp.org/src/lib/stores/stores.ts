import { writable } from 'svelte/store';
import type { Card } from '$domain/card/card';

/**
 * Core Application Stores
 * Strictly typed to prevent cascading lint errors in .svelte files.
 */
export const cardStore = writable<Card[]>([]);
export const searchStore = writable<string>('');
export const selectedEdition = writable<string>('webapp');
export const selectedVersion = writable<string>('2.2');
export const selectedLanguage = writable<string>('en');

export const resetAll = (): void => {
  cardStore.set([]);
  searchStore.set('');
};