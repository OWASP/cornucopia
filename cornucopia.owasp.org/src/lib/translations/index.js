
import i18n from 'sveltekit-i18n';
import en from './en';
import es from './es';
import uk from './uk';
import lang from './lang';

/** @type {import('sveltekit-i18n').Config} */
const config = {
  log: {
    level: 'warn',
  },
  translations: {
    en: {
      ...en,
      lang,
    },
    es: {
      ...es,
      lang,
    },
    uk: {
      ...uk,
      lang,
    },
  },
};

export const defaultLocale = 'en';
export const { t, locale, locales, loading, setLocale, translations } = new i18n(config);
