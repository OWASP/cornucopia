import { ZERO, ONE, FOUR, SIX, EIGHT } from '$lib/constants'

export function Capitalize (input: string): string {
  if (input === '') return ''
  const words = input.split(' ')
  for (let i = ZERO; i < words.length; i++) {
    if (words[i].length > ZERO) {
      words[i] = words[i].slice(ZERO, ONE).toUpperCase() + words[i].slice(ONE, input.length)
    }
  }
  return words.join(' ').replaceAll(' And ', ' and ').replaceAll(' Of ', ' of ')
}

export function Format (input: string): string {
  if (input === '') return ''
  return Capitalize(input.replaceAll('-', ' '))
}

export function FormatPlain (input: string): string {
  if (input === '') return ''
  return input.replaceAll('-', ' ')
}

export function convertToTitleCase (str: string): string {
  if (str === '') return ''
  return str.toLowerCase().replace(/\b\w/g, (char) => char.toUpperCase())
}

export function FormatDate (input: string): string {
  if (input === '') return ''
  const year = parseInt(input.substring(ZERO, FOUR), 10)
  const month = parseInt(input.substring(FOUR, SIX), 10)
  const day = parseInt(input.substring(SIX, EIGHT), 10)
  const date = new Date(year, month - ONE, day)
  return `${date.getDate()} ${date.toLocaleString('en-US', { month: 'short' })}, ${date.getFullYear()}`
}

export function FormatDateAsDate (date: Date | null): string {
  if (date === null) return ''
  return `${date.getDate()} ${date.toLocaleString('en-US', { month: 'short' })}, ${date.getFullYear()} ${date.getUTCHours()}:${date.getUTCMinutes()}:${date.getUTCSeconds()} UTC`
}

export function DisplayLink (input: string): string {
  if (input === '') return ''
  return input.trim().replaceAll('https', '').replaceAll('http', '').replaceAll('://', '')
}

export const Text = { Capitalize, Format, FormatPlain, convertToTitleCase, FormatDate, FormatDateAsDate, DisplayLink }