const RTL_LANGUAGES = ['fa', 'ar', 'he', 'ur'];
// languages whose concept/explanation markdown is NOT translated (falls back to English)
const LANGUAGES_WITHOUT_MARKDOWN = ['fa'];

export function getDirection(lang?: string): 'rtl' | 'ltr' {
  return RTL_LANGUAGES.includes(lang ?? '') ? 'rtl' : 'ltr';
}

export function contentLang(lang?: string): string {
  return LANGUAGES_WITHOUT_MARKDOWN.includes(lang ?? '') ? 'en' : (lang ?? 'en');
}