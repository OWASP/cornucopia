import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { load as parse } from 'js-yaml';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const APP_YAML = path.resolve(__dirname, '../application.yaml');
const SOURCE_DIR = path.resolve(__dirname, '../../source');

/**
 * Returns the full parsed application config from application.yaml
 */
function getAppConfig() {
  const content = fs.readFileSync(APP_YAML, 'utf-8');
  return parse(content);
}

/**
 * Reads application.yaml and returns parsed decks array
 */
function getDecks() {
  return getAppConfig().decks;
}

/**
 * Scans source/ directory and returns available languages
 * per edition and version, excluding draft languages.
 */
function getAvailableLanguages(edition, version, draftLanguages = []) {
  const files = fs.readdirSync(SOURCE_DIR);
  const langs = [];

  for (const file of files) {
    const match = file.match(
      new RegExp(`^${edition}-cards-${version.replace('.', '\\.')}-([a-z]{2}(?:_[a-z]{2})?)\\.yaml$`)
    );
    if (match) {
      const lang = match[1];
      if (!draftLanguages.includes(lang)) {
        langs.push(lang);
      }
    }
  }

  return langs;
}

/**
 * Generates edition routes for svelte prerender entries.
 */
function getEditionRoutes() {
  const decks = getDecks();
  const routes = [];

  for (const deck of decks) {
    if (deck.external) continue;

    for (const versionEntry of deck.versions) {
      const version = versionEntry.version;
      const draftLanguages = versionEntry.draftLanguages || [];
      const langs = getAvailableLanguages(deck.edition, version, draftLanguages);
      const card = deck.defaultPreviewCard;

      for (const lang of langs) {
        if (deck.edition === 'webapp' && version === '2.2' && lang === 'en') {
          routes.push(`/edition/${deck.edition}/${card}/${version}`);
        } else {
          routes.push(`/edition/${deck.edition}/${card}/${version}/${lang}`);
        }
      }
    }
  }

  return routes;
}

/**
 * Generates API routes for svelte prerender entries and headers.
 */
function getApiRoutes() {
  const decks = getDecks();
  const routes = [];

  for (const deck of decks) {
    if (deck.external) continue;

    for (const versionEntry of deck.versions) {
      const version = versionEntry.version;
      const draftLanguages = versionEntry.draftLanguages || [];

      routes.push(`/api/lang/${deck.edition}/${version}`);

      const langs = getAvailableLanguages(deck.edition, version, draftLanguages);
      for (const lang of langs) {
        const creRoute = `/api/cre/${deck.edition}/${lang}`;
        if (!routes.includes(creRoute)) {
          routes.push(creRoute);
        }
      }

      routes.push(`/api/mapping/${deck.edition}/${version}`);
    }

    if (deck.standards?.asvs) {
      for (const version of Object.keys(deck.standards.asvs.versionMap)) {
        const asvsFile = path.resolve(SOURCE_DIR, `${deck.edition}-asvs-${version}.yaml`);
        if (fs.existsSync(asvsFile)) {
          routes.push(`/api/asvs/${deck.edition}/${version}`);
        }
      }
    }
    if (deck.standards?.capec) {
      routes.push(`/api/capec/${deck.edition}/${deck.standards.capec.minVersion}`);
    }
  }

  const staticRoutes = [
    '/api/mastg/mobileapp/2.0',
    '/api/maswe/mobileapp/2.0',
    '/api/lang/dbd/1.0',
    '/api/cre/dbd/en',
  ];

  for (const r of staticRoutes) {
    if (!routes.includes(r)) routes.push(r);
  }

  return routes;
}

/**
 * Returns all svelte prerender entries.
 */
function getSvelteEntries(cardEntries) {
  return [
    ...cardEntries,
    '/404',
    '/api/docs',
    ...getEditionRoutes(),
    ...getApiRoutes(),
  ];
}

export { getDecks, getAvailableLanguages, getEditionRoutes, getApiRoutes, getSvelteEntries, getAppConfig };