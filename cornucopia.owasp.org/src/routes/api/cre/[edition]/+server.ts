import { DeckService } from '$lib/services/deckService';
import { json, error, type RequestHandler } from '@sveltejs/kit';
import { CreController } from '$domain/cre/creController';

export const prerender = false;

export const GET: RequestHandler = ({ params }) => {
  const edition = params.edition;
  
  // V16.5: Fail securely by terminating handler on invalid edition
  if (!edition || !DeckService.hasEdition(edition)) {
    throw error(404, 'Edition not found. Only: ' + DeckService.getLatestEditions().join(', ') + ' are supported.');
  }

  return json(
    {
      meta: {
        edition: CreController.getEditionName(edition),
        component: "cards",
        language: "en",
        languages: DeckService.getLanguages(edition),
        version: DeckService.getLatestVersion(edition),
      }
    },
    {
      headers: {
        'Content-Type': 'application/json'
      }
    }
  );
};
