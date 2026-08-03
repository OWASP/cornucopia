import { beforeEach, describe, expect, it, vi } from 'vitest';
import { loadApp } from './appHarness';

type CapabilityHook = {
  ExchangePlayerCapability: { mounted: () => void };
};

const mountCapabilityHook = (
  hooks: CapabilityHook,
  capability: unknown
) => {
  hooks.ExchangePlayerCapability.mounted.call({
    handleEvent: (
      _event: string,
      callback: (payload: { capability: unknown }) => void
    ) => callback({ capability })
  });
};

describe('player capability exchange error handling', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    document.body.innerHTML = '';
    document.head.innerHTML = '';
  });

  it('handles a rejected capability exchange without navigating', async () => {
    const assign = vi.fn();
    vi.stubGlobal(
      'location',
      { host: 'localhost:3000', assign } as unknown as Location
    );

    const { config } = await loadApp();
    const hooks = config.hooks as CapabilityHook;
    const fetchMock = vi.fn().mockResolvedValue({ ok: false });
    const warnSpy = vi.spyOn(console, 'warn').mockImplementation(() => undefined);
    vi.stubGlobal('fetch', fetchMock);

    mountCapabilityHook(hooks, 'signed-player-capability');

    await vi.waitFor(() => expect(warnSpy).toHaveBeenCalled());

    expect(fetchMock).toHaveBeenCalledOnce();
    expect(assign).not.toHaveBeenCalled();
  });

  it('rejects an invalid redirect returned by the exchange endpoint', async () => {
    const assign = vi.fn();
    vi.stubGlobal(
      'location',
      { host: 'localhost:3000', assign } as unknown as Location
    );

    const { config } = await loadApp();
    const hooks = config.hooks as CapabilityHook;
    const warnSpy = vi.spyOn(console, 'warn').mockImplementation(() => undefined);
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        json: vi.fn().mockResolvedValue({ redirect_to: 'https://example.org' })
      })
    );

    mountCapabilityHook(hooks, 'signed-player-capability');

    await vi.waitFor(() => expect(warnSpy).toHaveBeenCalled());
    expect(assign).not.toHaveBeenCalled();
  });

  it.each([['empty', ''], ['non-string', undefined]])(
    'ignores a %s capability',
    async (_description, capability) => {
      vi.stubGlobal('location', { host: 'localhost:3000' } as Location);

      const { config } = await loadApp();
      const hooks = config.hooks as CapabilityHook;
      const fetchMock = vi.fn();
      vi.stubGlobal('fetch', fetchMock);

      mountCapabilityHook(hooks, capability);

      await Promise.resolve();
      expect(fetchMock).not.toHaveBeenCalled();
    }
  );

  it('does not exchange a capability when the CSRF token is missing', async () => {
    vi.stubGlobal('location', { host: 'localhost:3000' } as Location);

    const { config } = await loadApp();
    const hooks = config.hooks as CapabilityHook;
    const fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
    document.querySelector('meta[name="csrf-token"]')?.remove();

    mountCapabilityHook(hooks, 'signed-player-capability');

    await Promise.resolve();
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
