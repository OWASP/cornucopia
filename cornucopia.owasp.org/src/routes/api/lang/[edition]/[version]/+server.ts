import { DeckService } from '$lib/services/deckService';
import { json, error, type RequestHandler } from '@sveltejs/kit';

export const prerender = true;

export const GET: RequestHandler = ({ params }) => {
  const edition = params.edition;
  const version = params.version;

  if (!edition || !DeckService.hasEdition(edition)) {
    throw error(404, 'Edition not found. Only: ' + DeckService.getLatestEditions().join(', ') + ' are supported.');
  }

  if (!version || !DeckService.hasVersion(edition, version)) {
    throw error(404, 'Version not found for edition ' + edition + '. Only: ' + DeckService.getVersions(edition).join(', ') + ' are supported.');
  }

  return json(
    {
      meta: {
        component: "cards",
        language: "all",
        languages: DeckService.getLanguagesForEditionVersion(edition, version),
        version
      }
    },
    {
      headers: {
        'Content-Type': 'application/json'
      }
    }
  );
};