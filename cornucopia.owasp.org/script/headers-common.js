import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { load as parse } from 'js-yaml';
import { getApiRoutes } from './app-config.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const DECKS_YAML = path.resolve(__dirname, '../decks.yaml');

function getCloudflareHeaders() {
  const content = fs.readFileSync(DECKS_YAML, 'utf-8');
  const { cloudflare } = parse(content);
  return cloudflare.headers;
}

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

function renderHeaderBlock(routePath, headers) {
  const lines = [routePath];
  for (const [key, value] of Object.entries(headers)) {
    lines.push(`  ${key}: ${value}`);
  }
  return lines.join('\n');
}

export function writeHeaders({
  buildDir,
  origin,
  includeGlobalRobotsTag = false,
  includeNotFound = false
}) {
  const headers = getCloudflareHeaders();

  const envBlock =
    origin === 'https://cornucopia.owasp.org'
      ? headers.production
      : headers.stage;

  const allHeaders = headers.all['/*'];
  const envGlobalHeaders = envBlock['/*'] || {};

  const merged = { ...allHeaders, ...envGlobalHeaders };
  if (includeGlobalRobotsTag) {
    merged['X-Robots-Tag'] = 'noindex';
  }

  const globalBlock = renderHeaderBlock('/*', merged);

  const notFoundBlock = includeNotFound
    ? '\n/404\n  X-Robots-Tag: noindex'
    : '';

  const resetLines = (headers.reset || []).map(r => `  ${r}`).join('\n');
  const apiBlock = apiPaths.map((apiPath) => [
    apiPath,
    resetLines,
    '  Access-Control-Allow-Origin: *',
    '  Content-Type: application/json; charset=UTF-8'
  ].join('\n')).join('\n');

  fs.writeFileSync(
    path.join(buildDir, '_headers'),
    `${globalBlock}${notFoundBlock}\n${apiBlock}\n`
  );
}