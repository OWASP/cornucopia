import fs from 'fs';
import path from 'path';
import { getApiRoutes, getAppConfig } from './app-config.js';

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

/**
 * @param {unknown} value
 * @returns {value is Record<string, unknown>}
 */
function isRecord(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

/**
 * @param {unknown} value
 * @returns {value is Record<string, Record<string, string>>}
 */
function isHeaderRules(value) {
  return isRecord(value) && Object.values(value).every(
    headers => isRecord(headers) && Object.values(headers).every(header => typeof header === 'string')
  );
}

/**
 * @param {string} routePath
 * @param {Record<string, string>} headers
 * @param {string[]} resets
 */
function renderHeaderBlock(routePath, headers, resets = []) {
  const lines = [routePath];
  for (const reset of resets) {
    if (Object.hasOwn(headers, reset.replace(/^! /, ''))) {
      lines.push(`  ${reset}`);
    }
  }
  for (const [key, value] of Object.entries(headers)) {
    lines.push(`  ${key}: ${value}`);
  }
  return lines.join('\n');
}

/**
 * @param {{ buildDir: string, environment: 'stage' | 'production' }} options
 */
export function writeHeaders({ buildDir, environment }) {
  const config = getAppConfig();
  if (!isRecord(config) || !isRecord(config.cloudflare) || !isRecord(config.cloudflare.headers)) {
    throw new Error('Missing Cloudflare headers in application.yaml');
  }
  const headers = config.cloudflare.headers;
  const envHeaders = headers[environment];
  if (envHeaders === undefined) {
    throw new Error(`Missing Cloudflare headers for environment: ${environment}`);
  }
  if (!isHeaderRules(headers.all) || !isHeaderRules(envHeaders)) {
    throw new Error(`Invalid Cloudflare header rules for environment: ${environment}`);
  }

  const resets = headers.reset ?? [];
  if (!Array.isArray(resets) || !resets.every(reset => typeof reset === 'string' && reset.startsWith('! '))) {
    throw new Error('Invalid Cloudflare header reset directives in application.yaml');
  }
  const blocks = [renderHeaderBlock('/*', {
    ...headers.all['/*'],
    ...envHeaders['/*']
  })];
  const routePaths = new Set([...Object.keys(headers.all), ...Object.keys(envHeaders)]);

  for (const routePath of routePaths) {
    if (routePath === '/*' || routePath === '/api/*') continue;
    blocks.push(renderHeaderBlock(routePath, {
      ...headers.all[routePath],
      ...envHeaders[routePath]
    }, resets));
  }

  // Expand JSON headers to known API endpoints so /api/docs keeps its HTML MIME type.
  const apiHeaders = { ...headers.all['/api/*'], ...envHeaders['/api/*'] };
  for (const apiPath of apiPaths) {
    blocks.push(renderHeaderBlock(apiPath, apiHeaders, resets));
  }

  fs.writeFileSync(
    path.join(buildDir, '_headers'),
    `${blocks.join('\n')}\n`
  );
}
