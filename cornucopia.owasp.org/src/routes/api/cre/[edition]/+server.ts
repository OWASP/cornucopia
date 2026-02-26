import { DeckService } from '$lib/services/deckService';
import { json, error, type RequestHandler } from '@sveltejs/kit';

// Prerendering this route would conflict with [edition]/[lang]/+server.ts
// because the static adapter cannot save both a file and directory at the
// same path. The post-build script (generate-edition-meta.js) handles
// generating the static output for production builds instead.
export const prerender = false;

const editions = ["webapp", "mobileapp"];

const editionNames: Record<string, string> = {
  webapp: "OWASP Cornucopia Website App Edition",
  mobileapp: "OWASP Cornucopia Mobile App Edition",
};

export const GET: RequestHandler = ({ params }) => {
  const edition = params.edition;
  if (!edition || !editions.includes(edition))
    error(404, 'Edition not found. Only: ' + editions.join(', ') + ' are supported.');

  return json({
    meta: {
      edition: editionNames[edition],
      component: "cards",
      language: "all",
      languages: DeckService.getLanguages(edition),
      version: DeckService.getLatestVersion(edition),
    }
  });
};
