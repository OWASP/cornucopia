import { defaultLocale, i18n } from '$lib/translations';
/** @type {import('@sveltejs/kit').Handle} */

export const handle = async ({ event, resolve }) => {
  const { url: _url, request } = event;

  // Get defined locales
  const supportedLocales = i18n.locales.map((l) => l.toLowerCase());

  // Get user preferred locale
  let userLocale = request.headers.get('accept-language') || defaultLocale;

  // Set default locale if user preferred locale does not match
  if (!supportedLocales.includes(userLocale)) userLocale = defaultLocale;
  await i18n.loadTranslations(userLocale);

  // Add html `lang` attribute
  const response = await resolve(
    { ...event, locals: { lang: userLocale, translation: i18n.translations[userLocale], fallbackTranslation: i18n.translations[defaultLocale] } },
    {
      transformPageChunk: ({ html }) =>
        html
          .replace(/<html.*>/, `<html lang="${userLocale}">`)
          .replaceAll(/<script([^>]*)>/gi, `<script nonce="DhcnhD3khTMePgXw"$1>`),
    }
  );

  const securityHeaders = {
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
    'Cross-Origin-Embedder-Policy': 'require-corp',
    'Cross-Origin-Opener-Policy': 'same-origin',
    'X-XSS-Protection': '1; mode=block',
    'X-Frame-Options': 'SAMEORIGIN',
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'same-origin',
    'Permissions-Policy':
      'accelerometer=(), autoplay=(), camera=(), document-domain=(), encrypted-media=(), fullscreen=(self "https://www.youtube.com/"), gyroscope=(), interest-cohort=(), magnetometer=(), microphone=(), midi=(), payment=(), picture-in-picture=(), publickey-credentials-get=(), sync-xhr=(), usb=(), xr-spatial-tracking=(), geolocation=()',
  };

  Object.entries(securityHeaders).forEach(([header, value]) => response.headers.set(header, value));

  return response;
};
