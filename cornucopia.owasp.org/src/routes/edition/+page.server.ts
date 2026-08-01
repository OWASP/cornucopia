import { redirect } from '@sveltejs/kit';

export function load({ params: _params }) {
  redirect(308, '/cards');
}
