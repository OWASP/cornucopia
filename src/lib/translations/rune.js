export const rune = (
    translation,
    fallback
) => {
    const _translation = translation;
    const _fallback = fallback;

    const _rune = {
        get () {
            return (name) => _translation[name] || _fallback[name];
        }
    }
    return _rune
};