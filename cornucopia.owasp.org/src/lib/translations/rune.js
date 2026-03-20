/* eslint-disable @typescript-eslint/explicit-function-return-type -- This is a JavaScript file; TypeScript return type syntax is not valid here. */
/**
 * @param {Record<string, string>} translation
 * @param {Record<string, string>} fallback
 * @returns {{ get: () => (name: string) => string }}
 */
export const rune = (translation, fallback) => ({
  get () {
    return (/** @type {string} */ name) => translation[name] ?? fallback[name]
  }
})