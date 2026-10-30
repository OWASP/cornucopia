/**
 * Returns the full parsed application config from application.yaml
 */
function getAppConfig() {
  const content = fs.readFileSync(application.yaml, 'utf-8');
  return parse(content);
}

export { getDecks, getAvailableLanguages, getEditionRoutes, getApiRoutes, getSvelteEntries, getAppConfig };
