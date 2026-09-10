import fs from 'fs';
import path from 'path';

export const apiPaths = [
  '/api/lang/mobileapp/1.1',
  '/api/lang/mobileapp/2.0',
  '/api/lang/webapp/2.2',
  '/api/lang/webapp/3.0',
  '/api/lang/dbd/1.0',
  '/api/lang/companion/1.0',
  '/api/lang/eop/5.0',
  '/api/asvs/webapp/3.0',
  '/api/capec/webapp/3.0',
  '/api/mastg/mobileapp/2.0',
  '/api/maswe/mobileapp/2.0',
  '/api/mapping/eop/5.0',
  '/api/mapping/webapp/2.2',
  '/api/mapping/webapp/3.0',
  '/api/mapping/mobileapp/1.1',
  '/api/mapping/mobileapp/2.0',
  '/api/mapping/companion/1.0',
  '/api/cre/mobileapp/en',
  '/api/cre/mobileapp/ru',
  '/api/cre/mobileapp/hi',
  '/api/cre/mobileapp/uk',
  '/api/cre/webapp/en',
  '/api/cre/webapp/es',
  '/api/cre/webapp/fr',
  '/api/cre/webapp/nl',
  '/api/cre/webapp/no_nb',
  '/api/cre/webapp/it',
  '/api/cre/webapp/pt_pt',
  '/api/cre/webapp/pt_br',
  '/api/cre/webapp/ru',
  '/api/cre/companion/en',
  '/api/cre/dbd/en',
  '/api/cre/eop/en',
  '/api/cre/eop/es',
  '/api/cre/eop/ru'
];

export function getBuildDir() {
  const root = path.resolve();

  for (const directory of ['.vercel/output', 'build', 'output']) {
    const buildDir = path.join(root, directory);
    if (fs.existsSync(buildDir)) {
      return buildDir;
    }
  }

  return undefined;
}

export function writeHeaders({
  buildDir,
  origin,
  includeGlobalRobotsTag = false,
  includeNotFound = false
}) {
  const globalHeaders = [
    '/*',
    `  Access-Control-Allow-Origin: ${origin}`,
    '  Cross-Origin-Opener-Policy: same-origin',
    ...(includeGlobalRobotsTag ? ['  X-Robots-Tag: noindex'] : []),
    '  X-Frame-Options: SAMEORIGIN',
    '  X-XSS-Protection: 1; mode=block',
    '  X-Content-Type-Options: nosniff',
    '  Referrer-Policy: same-origin',
    '  Permissions-Policy: accelerometer=(), autoplay=(), camera=(), document-domain=(), encrypted-media=(), fullscreen=(self "https://www.youtube.com/"), gyroscope=(), interest-cohort=(), magnetometer=(), microphone=(), midi=(), payment=(), picture-in-picture=(self "https://www.youtube.com/"), publickey-credentials-get=(), sync-xhr=(), usb=(), xr-spatial-tracking=(), geolocation=()',
    '  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload',
    "  Content-Security-Policy: base-uri 'self'; default-src 'none'; frame-src 'self' www.youtube.com youtube.com; connect-src 'self'; img-src 'self' i.ytimg.com; script-src 'self' 'nonce-DhcnhD3khTMePgXw'; style-src 'self'; style-src-elem 'self'; upgrade-insecure-requests"
  ].join('\n');

  const notFoundHeaders = includeNotFound
    ? '\n/404\n  X-Robots-Tag: noindex'
    : '';
  const apiHeaders = apiPaths.map((apiPath) => [
    apiPath,
    '  ! Access-Control-Allow-Origin',
    '  Access-Control-Allow-Origin: *',
    '  ! Content-Type',
    '  Content-Type: application/json; charset=UTF-8'
  ].join('\n')).join('\n');

  fs.writeFileSync(
    path.join(buildDir, '_headers'),
    `${globalHeaders}${notFoundHeaders}\n${apiHeaders}\n`
  );
}
