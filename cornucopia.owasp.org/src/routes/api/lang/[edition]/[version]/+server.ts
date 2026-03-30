import { DeckService } from '$lib/services/deckService';
import { json, error, type RequestHandler } from '@sveltejs/kit';
import { HTTP_STATUS } from '$lib/constants';

export const prerender = true;

export const GET: RequestHandler = ({ params }) => {
  const edition = String(params.edition);
  const version = String(params.version);

  if (!DeckService.hasEdition(edition)) {
    error(HTTP_STATUS.NOT_FOUND, `Edition not found. Only: ${DeckService.getLatestEditions().join(', ')} are supported.`);
  }

  if (!DeckService.hasVersion(edition, version)) {
    error(HTTP_STATUS.NOT_FOUND, `Version not found for edition ${edition}. Only: ${DeckService.getVersions(edition).join(', ')} are supported.`);
  }

  return json(
    {
      meta: {
        component: 'cards',
        language: 'all',
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