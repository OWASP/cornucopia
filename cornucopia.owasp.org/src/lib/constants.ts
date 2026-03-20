// HTTP status codes used across the application
/* eslint-disable @typescript-eslint/no-magic-numbers -- These are well-known constants */
export const HTTP_STATUS = {
  OK: 200,
  PERMANENT_REDIRECT: 308,
  NOT_FOUND: 404,
  INTERNAL_SERVER_ERROR: 500,
  BAD_REQUEST: 400,
  FOUND: 302,
} as const

export const CACHE = {
  KB: 1024,
  TIMEOUT_MS: 1000,
  NO_RESULT: -1,
} as const

export const PAGINATION = {
  PAGE_SIZE: 20,
} as const

export const CARD = {
  MIN_VERSION: 3.0,
} as const

export const ZERO = 0
export const ONE = 1
export const TWO = 2
export const FOUR = 4
export const SIX = 6
export const EIGHT = 8
/* eslint-enable @typescript-eslint/no-magic-numbers */