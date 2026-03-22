import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from '@sveltejs/kit';
import { CreController } from '$domain/cre/creController';
import fs from 'fs';
import yaml from 'js-yaml';
import path from 'path';

export const prerender = true;

export const GET: RequestHandler = () => {
  const cardFile = path.resolve('..', 'source', 'dbd-cards-1.0-en.yaml');
  let raw: any;
  try {
    raw = yaml.load(fs.readFileSync(cardFile, 'utf8'), { schema: yaml.FAILSAFE_SCHEMA });
  } catch {
    throw error(500, 'Failed to load DBD card data.');
  }

  if (!raw?.suits) throw error(500, 'Invalid card data format.');

  const data: { id: string; desc: string }[] = [];
  for (const suit of raw['suits']) {
    for (const card of suit['cards']) {
      data.push({ id: card['id'], desc: card['desc'] });
    }
  }

  return json(
    {
      meta: {
        edition: CreController.getEditionName('dbd'),
        component: 'cards',
        language: 'en',
        version: '1.0'
      },
      data
    },
    {
      headers: {
        'Content-Type': 'application/json'
      }
    }
  );
};
