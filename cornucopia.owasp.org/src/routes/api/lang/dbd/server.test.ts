import { describe, it, expect } from 'vitest';
import { GET } from './+server';

describe('GET /api/lang/dbd', () => {
  it('returns language metadata for dbd edition', async () => {
    const response = await GET({} as any);

    expect(response.status).toBe(200);
    expect(response.headers.get('content-type')).toContain('application/json');

    const body = await response.json();
    expect(body).toEqual({
      meta: {
        component: 'cards',
        language: 'all',
        languages: ['en'],
        version: '1.0'
      }
    });
  });
});
