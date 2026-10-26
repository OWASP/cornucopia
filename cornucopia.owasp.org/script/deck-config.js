import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { load as parse } from 'js-yaml';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const DECKS_YAML = path.resolve(__dirname, '../decks.yaml');
const SOURCE_DIR = path.resolve(__dirname, '../../source');

/**
 * Reads decks.yaml and returns parsed decks array
 */
function getDecks() {
  const content = fs.readFileSync(DECKS_YAML, 'utf-8');
  const { decks } = parse(content);
  return decks;
}

/**
 * Scans source/ directory and returns available languages
 * per edition and version, excluding draft languages.
 *
 * Source files follow the pattern: {edition}-cards-{version}-{lang}.yaml
 */
function getAvailableLanguages(edition, version, draftLanguages = []) {
  const files = fs.readdirSync(SOURCE_DIR);
  const langs = [];

  for (const file of files) {
    // Match pattern: {edition}-cards-{version}-{lang}.yaml
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
 * Generates /edition/{edition}/{defaultPreviewCard}/{version}/{lang} entries
 * for svelte.config.js prerender entries.
 * webapp/2.2 is special Ã¢â‚¬â€ it has no /en suffix in the route.
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
        // webapp 2.2 uses routes without /en (English is default, no lang suffix)
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
 * Generates API routes for both svelte.config.js entries
 * and headers-common.js apiPaths.
 */
function getApiRoutes() {
  const decks = getDecks();
  const routes = [];

  for (const deck of decks) {
    if (deck.external) continue;

    for (const versionEntry of deck.versions) {
      const version = versionEntry.version;
      const draftLanguages = versionEntry.draftLanguages || [];

      // /api/lang/{edition}/{version}
      routes.push(`/api/lang/${deck.edition}/${version}`);

      // /api/cre/{edition}/{lang}
      const langs = getAvailableLanguages(deck.edition, version, draftLanguages);
      for (const lang of langs) {
        const creRoute = `/api/cre/${deck.edition}/${lang}`;
        if (!routes.includes(creRoute)) {
          routes.push(creRoute);
        }
      }

      // /api/mapping/{edition}/{version}
      routes.push(`/api/mapping/${deck.edition}/${version}`);
    }

    // Standards-based routes - only add ASVS route if source file exists
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

  // Static routes that don't derive from decks
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
 * Returns all svelte prerender entries:
 * card entries (hardcoded, they don't change) + edition routes + api routes
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

export { getDecks, getAvailableLanguages, getEditionRoutes, getApiRoutes, getSvelteEntries };