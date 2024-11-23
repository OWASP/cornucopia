import { defaultLocale, locales, setLocale, locale, translations, loading } from '$lib/translations';
/** @type {import('@sveltejs/kit').Handle} */

export const handle = async ({ event, resolve }) => {
  const { url, request } = event;

  // Get defined locales
  const supportedLocales = locales.get().map((l) => l.toLowerCase());

  // Get user preferred locale
  let userLocale = request.headers.get('accept-language') || defaultLocale;

  // Set default locale if user preferred locale does not match
  if (!supportedLocales.includes(userLocale)) userLocale = defaultLocale;
  await loading.toPromise();
  await setLocale(userLocale);
  locale.set(userLocale);
  

  // Add html `lang` attribute
  return resolve({ ...event, locals: { lang: userLocale, translation: translations.get()[userLocale], fallbackTranslation: translations.get()[defaultLocale] } }, {
    transformPageChunk: ({ html }) => html.replace(/<html.*>/, `<html lang="${userLocale}">`),
  });
};
