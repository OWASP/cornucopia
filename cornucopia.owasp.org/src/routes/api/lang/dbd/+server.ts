import { json } from '@sveltejs/kit';
import type { RequestHandler } from '@sveltejs/kit';

export const prerender = true;

export const GET: RequestHandler = () => {
  return json(
    {
      meta: {
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
