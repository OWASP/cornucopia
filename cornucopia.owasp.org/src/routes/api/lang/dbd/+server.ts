import { json } from '@sveltejs/kit';
import type { RequestHandler } from '@sveltejs/kit';
import { CreController } from '$domain/cre/creController';

export const prerender = true;

export const GET: RequestHandler = () => {
  return json(
    {
      meta: {
        edition: CreController.getEditionName('dbd'),
        component: 'cards',
        language: 'all',
        languages: ['en'],
        version: '1.0'
      }
    },
    {
      headers: {
        'Content-Type': 'application/json'
      }
    }
  );
};
