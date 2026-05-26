import { error } from '@sveltejs/kit';

const SUPPORTED_LANGS = ['en', 'uk'];

const proxyRequest = async ({ params, url, request, fetch }) => {
  const lang = String(params.lang || '').toLowerCase();
  if (!SUPPORTED_LANGS.includes(lang)) {
    throw error(404);
  }

  const pathPart = params.path ? `/${params.path}` : '/';
  const target = new URL(pathPart + url.search, url.origin);
  const headers = new Headers(request.headers);
  headers.set('x-i18n-proxy', '1');
  headers.set('x-i18n-lang', lang);

  return fetch(new Request(target, {
    method: request.method,
    headers,
    body: request.body,
    duplex: request.body ? 'half' : undefined
  }));
};

export const GET = proxyRequest;
export const HEAD = proxyRequest;
