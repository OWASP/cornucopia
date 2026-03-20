/* eslint-disable @typescript-eslint/explicit-function-return-type -- JavaScript files do not support TypeScript return type syntax. */

/** @type {Record<string, Record<string, string> | undefined>} */
const translations = {};

/**
 * @param {string | null | undefined} lang
 * @param {string} key
 * @returns {string}
 */
export function t (lang, key) {
  const currentLang = lang ?? 'en';
  
  const { [currentLang]: dict } = translations;
  
  // Simplified to satisfy strict-boolean-expressions and unnecessary condition
  if (dict !== undefined) {
    return dict[key] ?? key;
  }
  
  return key;
}

export { translations };