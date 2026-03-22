import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { GET } from './+server';
import { CreController } from '$domain/cre/creController';

describe('GET /api/lang/dbd', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('returns language metadata for dbd edition', async () => {
    vi.spyOn(CreController, 'getEditionName').mockReturnValue(
      'Cornucopia Digital Benefits and Disbenefits Edition'
    );

    const response = await GET({} as any);

    expect(response.status).toBe(200);
    expect(response.headers.get('content-type')).toContain('application/json');

    const body = await response.json();
    expect(body).toEqual({
      meta: {
        edition: 'Cornucopia Digital Benefits and Disbenefits Edition',
        component: 'cards',
        language: 'all',
        languages: ['en'],
        version: '1.0'
      }
    });
  });
});
