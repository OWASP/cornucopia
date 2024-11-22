import { Text } from '$lib/utils/text.js';

export const prerender = true;

export async function load(event) 
{
    return {
        renderTimestamp : Text.FormatDateAsDate(new Date()),
        timestamp : new Date(),
        translation: event.locals.translation,
        fallbackTranslation: event.locals.fallbackTranslation,
        lang: event.locals.lang
    }
}