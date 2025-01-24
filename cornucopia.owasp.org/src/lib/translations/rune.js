export const rune = (
    /** @type {any} */ translation,
    /** @type {any} */ fallback
) => {
    const _translation = translation;
    const _fallback = fallback;

    const _rune = {
        get () {
            return (/** @type {string} */ name) => _translation[name] || _fallback[name];
        }
    }
    return _rune
};