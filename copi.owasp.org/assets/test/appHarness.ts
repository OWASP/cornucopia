import { vi } from 'vitest';

const state = vi.hoisted(() => {
  const topbar = {
    config: vi.fn(),
    show: vi.fn(),
    hide: vi.fn()
  };

  const dragula = vi.fn();
  const liveSocketInstances: Array<{
    url: string;
    socket: unknown;
    config: Record<string, unknown>;
    instance: { connect: ReturnType<typeof vi.fn> };
  }> = [];

  class LiveSocket {
    connect: ReturnType<typeof vi.fn>;

    constructor(url: string, socket: unknown, config: Record<string, unknown>) {
      this.connect = vi.fn();
      liveSocketInstances.push({ url, socket, config, instance: this });
    }
  }

  class Socket {}

  return { topbar, dragula, liveSocket: LiveSocket, liveSocketInstances, Socket };
});

vi.mock('phoenix_html', () => ({}));
vi.mock('phoenix', () => ({ Socket: state.Socket }));
vi.mock('../vendor/topbar', () => ({ default: state.topbar }));
vi.mock('../vendor/dragula', () => ({ default: state.dragula }));
vi.mock('phoenix_live_view', () => ({ LiveSocket: state.liveSocket }));

export { state };

export async function loadApp(body = '', csrf = 'test-csrf') {
  state.topbar.config.mockClear();
  state.topbar.show.mockClear();
  state.topbar.hide.mockClear();
  state.dragula.mockClear();
  state.liveSocketInstances.length = 0;
  document.head.innerHTML = `<meta name="csrf-token" content="${csrf}">`;
  document.body.innerHTML = body;

  await vi.resetModules();
  await import('../js/app.js');

  const latest = state.liveSocketInstances.at(-1);

  if (!latest) {
    throw new Error('LiveSocket was not initialized');
  }

  return latest;
}
