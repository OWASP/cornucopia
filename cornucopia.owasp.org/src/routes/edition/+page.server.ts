import { redirect } from '@sveltejs/kit'
import { HTTP_STATUS } from '$lib/constants'

export function load (): never {
  redirect(HTTP_STATUS.PERMANENT_REDIRECT, '/cards')
}