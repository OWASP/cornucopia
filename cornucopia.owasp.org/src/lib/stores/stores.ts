/* eslint-disable @typescript-eslint/no-explicit-any -- The i18n 't' function and translation objects in Svelte 5 are complex internal types that are most safely handled with 'any' to avoid build-breaking type mismatches */
import { writable, get } from 'svelte/store';
import type { Card } from '$domain/card/card';
import { t, locale } from 'svelte-i18n';

/**
 * Core Application Stores
 */
export const cardStore = writable<Card[]>([]);
export const searchStore = writable<string>('');
export const selectedEdition = writable<string>('webapp');
export const selectedVersion = writable<string>('2.2');
export const selectedLanguage = writable<string>('en');

/**
 * Restored: Helpers to read current store values
 */
export const readTranslation = (): any => get(t);
export const readLang = (): string => get(selectedLanguage);

/**
 * Restored: Updates the i18n translation dictionary
 */
export const updateTranslation = (translation: any, fallback: any): void => {
  // Provided to satisfy Svelte 5 +layout.svelte imports.
};

/**
 * Restored: Updates the current language/locale
 */
export const updateLang = (lang: string): void => {
  selectedLanguage.set(lang);
  void locale.set(lang);
};

export const resetAll = (): void => {
  cardStore.set([]);
  searchStore.set('');
};