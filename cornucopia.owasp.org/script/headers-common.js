import fs from 'fs';
import path from 'path';
import { getApiRoutes } from './deck-config.js';

export const apiPaths = getApiRoutes();

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
    "  Content-Security-Policy: base-uri 'self'; default-src 'none'; frame-src 'self' https://www.youtube.com youtube.com; connect-src 'self'; img-src 'self' i.ytimg.com; script-src 'self' 'nonce-DhcnhD3khTMePgXw'; style-src 'self'; style-src-elem 'self'; upgrade-insecure-requests"
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