import { redirect } from '@sveltejs/kit';
import { building } from '$app/environment';
import { defaultLocale, locales, setLocale, locale, translations, loading } from '$lib/translations';
/** @type {import('@sveltejs/kit').Handle} */

export const handle = async ({ event, resolve }) => {
  const { request } = event;
  const supportedLangs = ['en', 'es', 'uk'];
  const pathname = event.url.pathname;
  const pathMatch = pathname.match(/^\/(en|es|uk)(\/|$)/i);
  const proxiedLang = request.headers.get('x-i18n-lang')?.toLowerCase() || '';
  const isProxyRequest = request.headers.get('x-i18n-proxy') === '1';
  const isAssetOrApiPath =
    pathname.startsWith('/_app') ||
    pathname.startsWith('/api') ||
    pathname.startsWith('/build') ||
    pathname.endsWith('.html') ||
    pathname.startsWith('/cards') ||
    pathname.startsWith('/card') ||
    pathname === '/error' ||
    pathname === '/error/' ||
    pathname === '/404' ||
    pathname === '/404/' ||
    pathname === '/favicon.ico' ||
    pathname === '/robots.txt' ||
    pathname === '/rss.xml' ||
    pathname === '/sitemap.xml';

  if (!building && !pathMatch && !isAssetOrApiPath && !isProxyRequest) {
    const acceptLang = request.headers.get('accept-language') || '';
    const preferred = acceptLang.split(',')[0]?.split('-')[0]?.toLowerCase() || '';
    const selectedLang = supportedLangs.includes(preferred) ? preferred : 'en';
    const suffix = pathname === '/' ? '/' : pathname;
    throw redirect(302, `/${selectedLang}${suffix}`);
  }

  const requestedLang = supportedLangs.includes(proxiedLang)
    ? proxiedLang
    : pathMatch
      ? pathMatch[1].toLowerCase()
      : defaultLocale;

  // Get defined locales
  const supportedLocales = locales.get().map((l) => l.toLowerCase());
  const userLocale = supportedLocales.includes(requestedLang) ? requestedLang : defaultLocale;

  await loading.toPromise();
  await setLocale(userLocale);
  locale.set(userLocale);

  const currentTranslations = translations.get();
  const activeTranslation = currentTranslations[userLocale] || currentTranslations[defaultLocale];
  const fallbackTranslation = currentTranslations[defaultLocale];

  // Add html `lang` attribute
  const response = await resolve({ ...event, locals: { lang: requestedLang, translation: activeTranslation, fallbackTranslation } }, {
    transformPageChunk: ({ html }) => html.replace(/<html.*>/, `<html lang="${requestedLang}">`).replaceAll(/<script[^>]*>/gi, `<script nonce="DhcnhD3khTMePgXw">`),
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
