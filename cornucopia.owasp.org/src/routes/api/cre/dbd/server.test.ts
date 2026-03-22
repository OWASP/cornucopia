import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { GET } from './+server';
import { CreController } from '$domain/cre/creController';
import fs from 'fs';
import yaml from 'js-yaml';

vi.mock('fs');
vi.mock('js-yaml');

describe('GET /api/cre/dbd', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('returns card data for dbd edition', async () => {
    vi.spyOn(fs, 'readFileSync').mockReturnValue('mocked');
    vi.spyOn(yaml, 'load').mockReturnValue({
      suits: [
        {
          id: 'SCO',
          name: 'SCOPE',
          cards: [
            { id: 'SCO2', desc: 'Tommy does not create...' },
            { id: 'SCOA', desc: 'You have invented...' }
          ]
        }
      ]
    } as any);
    vi.spyOn(CreController, 'getEditionName').mockReturnValue(
      'Cornucopia Digital Benefits and Disbenefits Edition'
    );

    const response = await GET({} as any);

    expect(response.status).toBe(200);
    expect(response.headers.get('content-type')).toContain('application/json');

    const body = await response.json();
    expect(body.meta).toEqual({
      edition: 'Cornucopia Digital Benefits and Disbenefits Edition',
      component: 'cards',
      language: 'en',
      version: '1.0'
    });
    expect(body.data).toHaveLength(2);
    expect(body.data[0]).toEqual({ id: 'SCO2', desc: 'Tommy does not create...' });
  });
});
