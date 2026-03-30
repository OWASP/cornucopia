/* eslint-disable @typescript-eslint/explicit-function-return-type -- This is a JavaScript file; TypeScript return type syntax is not valid here. */
/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {
  const response = await resolve(event);
  return response;
}