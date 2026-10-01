import { I18n } from 'sveltekit-i18n';
import en from './en';
import es from './es';
import uk from './uk';
import lang from './lang';

/** @type {import('sveltekit-i18n').Config} */
export const config = {
  log: {
    level: 'warn',
  },
  translations: {
    en: { ...en, lang },
    es: { ...es, lang },
    uk: { ...uk, lang },
  },
  initLocale: 'en',
};

export const defaultLocale = 'en';
export const i18n = new I18n(config);
