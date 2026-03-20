import { writable } from 'svelte/store';
import type { Card } from '$domain/card/card';

export const selectedCards = writable<Card[]>([]);
export const currentLanguage = writable<string>('en');
export const currentEdition = writable<string>('webapp');

export const resetAllStores = (): void => {
    selectedCards.set([]);
    currentLanguage.set('en');
    currentEdition.set('webapp');
};