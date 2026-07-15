import { beforeEach, describe, expect, it, vi } from 'vitest';
import { loadApp, state } from './appHarness';

declare global {
  interface Window {
    liveSocket?: unknown;
  }
}

describe('assets/js/app.js', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    document.body.innerHTML = '';
    document.head.innerHTML = '';
  });

  it('initializes LiveSocket and topbar for local development', async () => {
    await vi.stubGlobal('location', { host: 'localhost:3000' } as Location);
    const { instance } = await loadApp();

    expect(state.topbar.config).toHaveBeenCalledWith({
      barColors: { 0: '#29d' },
      shadowColor: 'rgba(0, 0, 0, .3)'
    });
    expect(state.liveSocketInstances).toHaveLength(1);
    expect(state.liveSocketInstances[0].url).toBe('/live');
    expect(state.liveSocketInstances[0].config).toMatchObject({
      params: { _csrf_token: 'test-csrf' }
    });
    expect(state.liveSocketInstances[0].config).toHaveProperty('hooks');
    expect(instance.connect).toHaveBeenCalledTimes(1);
    expect(Reflect.get(window, 'liveSocket')).toBe(instance);
    expect(state.liveSocketInstances[0].config).toMatchObject({
      longPollFallbackMs: undefined
    });

    window.dispatchEvent(new Event('phx:page-loading-start'));
    window.dispatchEvent(new Event('phx:page-loading-stop'));
    expect(state.topbar.show).toHaveBeenCalledWith(300);
    expect(state.topbar.hide).toHaveBeenCalled();
  });

  it('uses long polling fallback outside localhost', async () => {
    await vi.stubGlobal('location', { host: 'example.com' } as Location);
    await loadApp();

    expect(state.liveSocketInstances[0].config).toMatchObject({
      longPollFallbackMs: 2500
    });
  });

  it('wires DragDrop handlers and posts played cards', async () => {
    await vi.stubGlobal('location', { host: 'localhost:3000' } as Location);
    document.body.innerHTML = `
      <div id="hand"></div>
      <div id="table">
        <section class="card-player">
          <div class="name">Drop a card</div>
        </section>
      </div>
    `;
    const { config } = await loadApp(document.body.innerHTML);
    const hooks = config.hooks as {
      DragDrop: { mounted: () => void };
    };

    const drake = {
      on: vi.fn(),
      cancel: vi.fn()
    };
    state.dragula.mockReturnValue(drake);

    hooks.DragDrop.mounted();

    expect(state.dragula).toHaveBeenCalledTimes(1);
    const options = state.dragula.mock.calls[0][1];

    expect(options.invalid({
      classList: { contains: () => false },
      dataset: { game: 'g1', player: 'p1', dealtcard: 'c1' }
    }, {
      closest: () => null,
      dataset: { game: 'g1', player: 'p1', dealtcard: 'c1' }
    })).toBe(false);
    expect(options.invalid({
      classList: { contains: () => true },
      dataset: { game: 'g1', player: 'p1', dealtcard: 'c1' }
    }, {
      closest: () => null,
      dataset: { game: 'g1', player: 'p1', dealtcard: 'c1' }
    })).toBe(true);

    expect(options.accepts(
      { dataset: { game: 'g1', player: 'p1', dealtcard: 'c1' } },
      { id: 'table' },
      { id: 'hand' }
    )).toBe(true);
    expect(options.accepts(
      { dataset: { game: 'g1', player: 'p1', dealtcard: 'c1' } },
      { id: 'table' },
      { id: 'table' }
    )).toBe(false);
    expect(options.accepts(
      { dataset: { game: 'g1', player: 'p1', dealtcard: 'c1' } },
      { id: 'aside' },
      { id: 'hand' }
    )).toBe(true);
    expect(options.accepts(
      { dataset: {} },
      { id: 'table' },
      { id: 'hand' }
    )).toBe(false);
    document.body.innerHTML = `
      <div id="hand"></div>
      <div id="table"></div>
    `;
    expect(options.accepts(
      { dataset: { game: 'g1', player: 'p1', dealtcard: 'c1' } },
      { id: 'table' },
      { id: 'hand' }
    )).toBe(true);
    document.body.innerHTML = `
      <div id="hand"></div>
      <div id="table">
        <section class="card-player">
          <div class="name">Your Card</div>
          <div>Already played</div>
        </section>
      </div>
    `;
    expect(options.accepts(
      { dataset: { game: 'g1', player: 'p1', dealtcard: 'c1' } },
      { id: 'table' },
      { id: 'hand' }
    )).toBe(false);

    const dropHandler = drake.on.mock.calls.find(([event]) => event === 'drop')?.[1] as
      | ((element: Element, target: HTMLElement, source: HTMLElement) => void)
      | undefined;

    expect(dropHandler).toBeTypeOf('function');

    const source = document.createElement('div');
    const element = document.createElement('div');
    element.dataset.game = 'game-1';
    element.dataset.player = 'player-1';
    element.dataset.dealtcard = 'deal-1';
    source.appendChild(element);

    const fetchMock = vi.fn().mockResolvedValue({ ok: true });
    vi.stubGlobal('fetch', fetchMock);

    dropHandler?.(element, document.getElementById('table') as HTMLElement, source);

    expect(fetchMock).toHaveBeenCalledWith(
      '/api/games/game-1/players/player-1/card',
      expect.objectContaining({
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ dealt_card_id: 'deal-1' })
      })
    );

    dropHandler?.(element, { id: 'sidebar' } as HTMLElement, source);
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it('reverts the card when the API returns a non-ok response', async () => {
    await vi.stubGlobal('location', { host: 'localhost:3000' } as Location);
    document.body.innerHTML = `
      <div id="hand"></div>
      <div id="table">
        <section class="card-player">
          <div class="name">Drop a card</div>
        </section>
      </div>
    `;
    const { config } = await loadApp(document.body.innerHTML);
    const hooks = config.hooks as {
      DragDrop: { mounted: () => void };
    };

    const drake = {
      on: vi.fn(),
      cancel: vi.fn()
    };
    state.dragula.mockReturnValue(drake);
    hooks.DragDrop.mounted();

    const dropHandler = drake.on.mock.calls.find(([event]) => event === 'drop')?.[1] as
      | ((element: Element, target: HTMLElement, source: HTMLElement) => void)
      | undefined;

    const source = document.createElement('div');
    const appendSpy = vi.spyOn(source, 'appendChild');
    const element = document.createElement('div');
    element.dataset.game = 'game-1';
    element.dataset.player = 'player-1';
    element.dataset.dealtcard = 'deal-1';
    source.appendChild(element);

    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false }));

    dropHandler?.(element, document.getElementById('table') as HTMLElement, source);

    await Promise.resolve();

    expect(appendSpy).toHaveBeenCalledWith(element);
  });

  it('handles rejected API calls without a source container', async () => {
    await vi.stubGlobal('location', { host: 'localhost:3000' } as Location);
    document.body.innerHTML = `
      <div id="hand"></div>
      <div id="table">
        <section class="card-player">
          <div class="name">Drop a card</div>
        </section>
      </div>
    `;
    const { config } = await loadApp(document.body.innerHTML);
    const hooks = config.hooks as {
      DragDrop: { mounted: () => void };
    };

    const drake = {
      on: vi.fn(),
      cancel: vi.fn()
    };
    state.dragula.mockReturnValue(drake);
    hooks.DragDrop.mounted();

    const dropHandler = drake.on.mock.calls.find(([event]) => event === 'drop')?.[1] as
      | ((element: Element, target: HTMLElement, source?: HTMLElement) => void)
      | undefined;

    const element = document.createElement('div');
    element.dataset.game = 'game-1';
    element.dataset.player = 'player-1';
    element.dataset.dealtcard = 'deal-1';

    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('network')));

    dropHandler?.(element, document.getElementById('table') as HTMLElement, undefined);

    await Promise.resolve();
    await Promise.resolve();

    expect(drake.cancel).not.toHaveBeenCalled();
  });

  it('cancels invalid drops without identifiers', async () => {
    await vi.stubGlobal('location', { host: 'localhost:3000' } as Location);
    document.body.innerHTML = `
      <div id="hand"></div>
      <div id="table">
        <section class="card-player">
          <div class="name">Drop a card</div>
        </section>
      </div>
    `;
    const { config } = await loadApp(document.body.innerHTML);
    const hooks = config.hooks as {
      DragDrop: { mounted: () => void };
    };

    const drake = {
      on: vi.fn(),
      cancel: vi.fn()
    };
    state.dragula.mockReturnValue(drake);
    hooks.DragDrop.mounted();

    const dropHandler = drake.on.mock.calls.find(([event]) => event === 'drop')?.[1] as
      | ((element: Element, target: HTMLElement, source: HTMLElement) => void)
      | undefined;

    const source = document.createElement('div');
    const element = document.createElement('div');
    source.appendChild(element);

    dropHandler?.(element, document.getElementById('table') as HTMLElement, source);

    expect(drake.cancel).toHaveBeenCalledWith(true);
  });

  it('restores the card when the API rejects the drop', async () => {
    await vi.stubGlobal('location', { host: 'localhost:3000' } as Location);
    document.body.innerHTML = `
      <div id="hand"></div>
      <div id="table">
        <section class="card-player">
          <div class="name">Drop a card</div>
        </section>
      </div>
    `;
    const { config } = await loadApp(document.body.innerHTML);
    const hooks = config.hooks as {
      DragDrop: { mounted: () => void };
    };

    const drake = {
      on: vi.fn(),
      cancel: vi.fn()
    };
    state.dragula.mockReturnValue(drake);
    hooks.DragDrop.mounted();

    const dropHandler = drake.on.mock.calls.find(([event]) => event === 'drop')?.[1] as
      | ((element: Element, target: HTMLElement, source: HTMLElement) => void)
      | undefined;

    const source = document.createElement('div');
    const element = document.createElement('div');
    element.dataset.game = 'game-1';
    element.dataset.player = 'player-1';
    element.dataset.dealtcard = 'deal-1';
    source.appendChild(element);

    const fetchMock = vi.fn().mockRejectedValue(new Error('network'));
    vi.stubGlobal('fetch', fetchMock);

    await dropHandler?.(element, document.getElementById('table') as HTMLElement, source);

    expect(source.contains(element)).toBe(true);
  });

  it('mounts CopyUrl and shows the copied state', async () => {
    await vi.stubGlobal('location', { host: 'localhost:3000' } as Location);
    document.body.innerHTML = `
      <div id="copy-url-container">
        <button id="copy-url-btn"></button>
        <input id="copied-url" value="https://example.org" />
        <span id="url-copied" class="hidden"></span>
      </div>
    `;
    const { config } = await loadApp(document.body.innerHTML);
    const hooks = config.hooks as {
      CopyUrl: { mounted: () => void };
    };

    const clipboardWrite = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, 'clipboard', {
      value: { writeText: clipboardWrite },
      configurable: true
    });

    hooks.CopyUrl.mounted.call({
      el: document.getElementById('copy-url-container')
    });

    document.getElementById('copy-url-btn')?.dispatchEvent(new Event('click'));

    await vi.waitFor(() => {
      expect(clipboardWrite).toHaveBeenCalledWith('https://example.org');
      expect(document.getElementById('url-copied')?.classList.contains('hidden')).toBe(false);
    });
  });

  it('persists the current player session for a game through the session endpoint', async () => {
    await vi.stubGlobal('location', { host: 'localhost:3000' } as Location);
    document.body.innerHTML = `
      <div
        id="player-session"
        data-game-id="01KXJS02XPBB679E2W70JGRV0Z"
        data-player-id="01KXJS0JYKW9MJHBNBXE07YPHF"
        data-store-player-session="true"
      ></div>
    `;
    const { config } = await loadApp(document.body.innerHTML);
    const hooks = config.hooks as {
      PersistPlayerSession: { mounted: () => void };
    };
    const fetchMock = vi.fn().mockResolvedValue({ ok: true });

    vi.stubGlobal('fetch', fetchMock);

    hooks.PersistPlayerSession.mounted.call({
      el: document.getElementById('player-session')
    });

    await Promise.resolve();

    expect(fetchMock).toHaveBeenCalledWith(
      '/api/games/01KXJS02XPBB679E2W70JGRV0Z/players/01KXJS0JYKW9MJHBNBXE07YPHF/session',
      expect.objectContaining({
        method: 'PUT',
        credentials: 'same-origin',
        cache: 'no-store'
      })
    );
  });

  it('clears the current player session through the session endpoint when persistence is disabled', async () => {
    await vi.stubGlobal('location', { host: 'localhost:3000' } as Location);
    document.body.innerHTML = `
      <div
        id="player-session"
        data-game-id="01KXJS02XPBB679E2W70JGRV0Z"
        data-player-id="01KXJS0JYKW9MJHBNBXE07YPHF"
        data-store-player-session="false"
      ></div>
    `;
    const { config } = await loadApp(document.body.innerHTML);
    const hooks = config.hooks as {
      PersistPlayerSession: { mounted: () => void };
    };
    const fetchMock = vi.fn().mockResolvedValue({ ok: true });

    vi.stubGlobal('fetch', fetchMock);

    hooks.PersistPlayerSession.mounted.call({
      el: document.getElementById('player-session')
    });

    await Promise.resolve();

    expect(fetchMock).toHaveBeenCalledWith(
      '/api/games/01KXJS02XPBB679E2W70JGRV0Z/player-session',
      expect.objectContaining({
        method: 'DELETE',
        credentials: 'same-origin',
        cache: 'no-store'
      })
    );
  });

  it('syncs the player session again when the hook is updated', async () => {
    await vi.stubGlobal('location', { host: 'localhost:3000' } as Location);
    document.body.innerHTML = `
      <div
        id="player-session"
        data-game-id="01KXJS02XPBB679E2W70JGRV0Z"
        data-player-id="01KXJS0JYKW9MJHBNBXE07YPHF"
        data-store-player-session="true"
      ></div>
    `;
    const { config } = await loadApp(document.body.innerHTML);
    const hooks = config.hooks as {
      PersistPlayerSession: { updated: () => void };
    };
    const fetchMock = vi.fn().mockResolvedValue({ ok: true });

    vi.stubGlobal('fetch', fetchMock);

    hooks.PersistPlayerSession.updated.call({
      el: document.getElementById('player-session')
    });

    await Promise.resolve();

    expect(fetchMock).toHaveBeenCalledWith(
      '/api/games/01KXJS02XPBB679E2W70JGRV0Z/players/01KXJS0JYKW9MJHBNBXE07YPHF/session',
      expect.objectContaining({
        method: 'PUT',
        credentials: 'same-origin',
        cache: 'no-store'
      })
    );
  });

  it('does not persist a player session when identifiers are malformed', async () => {
    await vi.stubGlobal('location', { host: 'localhost:3000' } as Location);
    document.body.innerHTML = `
      <div
        id="player-session"
        data-game-id="invalid"
        data-player-id="also-invalid"
        data-store-player-session="true"
      ></div>
    `;
    const { config } = await loadApp(document.body.innerHTML);
    const hooks = config.hooks as {
      PersistPlayerSession: { mounted: () => void };
    };
    const fetchMock = vi.fn().mockResolvedValue({ ok: true });

    vi.stubGlobal('fetch', fetchMock);

    hooks.PersistPlayerSession.mounted.call({
      el: document.getElementById('player-session')
    });

    await Promise.resolve();

    expect(fetchMock).not.toHaveBeenCalled();
  });

  it('does not persist a player session when the CSRF token is missing', async () => {
    await vi.stubGlobal('location', { host: 'localhost:3000' } as Location);
    document.head.innerHTML = '';
    document.body.innerHTML = `
      <div
        id="player-session"
        data-game-id="01KXJS02XPBB679E2W70JGRV0Z"
        data-player-id="01KXJS0JYKW9MJHBNBXE07YPHF"
        data-store-player-session="true"
      ></div>
    `;
    const { config } = await loadApp(document.body.innerHTML, '');
    const hooks = config.hooks as {
      PersistPlayerSession: { mounted: () => void };
    };
    const fetchMock = vi.fn().mockResolvedValue({ ok: true });

    vi.stubGlobal('fetch', fetchMock);

    document.querySelector('meta[name="csrf-token"]')?.remove();

    hooks.PersistPlayerSession.mounted.call({
      el: document.getElementById('player-session')
    });

    await Promise.resolve();

    expect(fetchMock).not.toHaveBeenCalled();
  });

  it('handles session endpoint failures without throwing', async () => {
    await vi.stubGlobal('location', { host: 'localhost:3000' } as Location);
    document.body.innerHTML = `
      <div
        id="player-session"
        data-game-id="01KXJS02XPBB679E2W70JGRV0Z"
        data-player-id="01KXJS0JYKW9MJHBNBXE07YPHF"
        data-store-player-session="true"
      </div>
    `;
    const { config } = await loadApp(document.body.innerHTML);
    const hooks = config.hooks as {
      PersistPlayerSession: { mounted: () => void };
    };
    const fetchMock = vi.fn().mockRejectedValue(new Error('network'));

    vi.stubGlobal('fetch', fetchMock);
    const warnSpy = vi.spyOn(console, 'warn').mockImplementation(() => undefined);

    hooks.PersistPlayerSession.mounted.call({
      el: document.getElementById('player-session')
    });

    await Promise.resolve();

    expect(warnSpy).toHaveBeenCalled();
  });

});
