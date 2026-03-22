import { json } from '@sveltejs/kit';
import type { RequestHandler } from '@sveltejs/kit';
import { CreController } from '$domain/cre/creController';
import fs from 'fs';
import yaml from 'js-yaml';
import path from 'path';

export const prerender = true;

const __dirname = path.resolve(path.dirname(''));

export const GET: RequestHandler = () => {
  const cardFile = `${__dirname}/../source/dbd-cards-1.0-en.yaml`;
  const raw = yaml.load(fs.readFileSync(cardFile, 'utf8'), { schema: yaml.FAILSAFE_SCHEMA }) as any;

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
