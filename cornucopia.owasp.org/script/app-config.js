/**
 * Returns the full parsed application config from decks.yaml
 */
function getAppConfig() {
  const content = fs.readFileSync(DECKS_YAML, 'utf-8');
  return parse(content);
}

export { getDecks, getAvailableLanguages, getEditionRoutes, getApiRoutes, getSvelteEntries, getAppConfig };
