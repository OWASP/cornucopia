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
  const response = await resolve({ ...event, locals: { lang: userLocale, translation: translations.get()[userLocale], fallbackTranslation: translations.get()[defaultLocale] } }, {
    transformPageChunk: ({ html }) => html.replace(/<html.*>/, `<html lang="${userLocale}">`),
  });

  const securityHeaders = {
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
    'Cross-Origin-Embedder-Policy': 'require-corp',
    'Cross-Origin-Opener-Policy': 'same-origin',
    'X-XSS-Protection': '1; mode=block',
    'X-Frame-Options': 'SAMEORIGIN',
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'same-origin',
    'Permissions-Policy': 'accelerometer=(), autoplay=(), camera=(), document-domain=(), encrypted-media=(), fullscreen=(self "https://www.youtube.com/"), gyroscope=(), interest-cohort=(), magnetometer=(), microphone=(), midi=(), payment=(), picture-in-picture=(), publickey-credentials-get=(), sync-xhr=(), usb=(), xr-spatial-tracking=(), geolocation=()'
  }

  Object.entries(securityHeaders).forEach(
    ([header, value]) => response.headers.set(header, value)
  );

  return response;
};
